from django.core.exceptions import ValidationError
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin, Group)
from django.core.validators import RegexValidator
from django.db import models, transaction
from django.utils import timezone
from django.utils.timezone import now
from simple_history.models import HistoricalRecords


class UserManager(BaseUserManager):
    @transaction.atomic
    def create_user(self, email, password=None, **extra_fields):
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        group = Group.objects.get(name='standard_user')
        user.groups.add(group)
        return user

    @transaction.atomic
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        group = Group.objects.get(name='superuser')
        user.groups.add(group)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    history = HistoricalRecords()

    def __str__(self):
        return f'{self.surname}_{self.name[:1]}'

    def display_group(self):
        return ', '.join(group.name for group in self.groups.all())


class BasicInformation(models.Model):
    created_at = models.DateField(auto_now_add=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, auto_created=User)
    updated_at = models.DateField(auto_now=True, editable=False)
    extra_info = models.TextField(max_length=250, blank=True)

    class Meta:
        abstract = True
        ordering = ('created_at',)
        verbose_name = "Basic information"
        verbose_name_plural = "Basic information"


class ProductSoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

    def soft_delete(self):
        self.update(is_deleted=True, deleted_at=timezone.now())


class SoftDelete(models.Model):
    is_deleted = models.BooleanField(default=False, blank=True)
    deleted_at = models.DateField(editable=False, blank=True, null=True)

    objects = ProductSoftDeleteManager()

    class Meta:
        abstract = True

    def delete(self):
        self.deleted_at = timezone.now()
        self.is_deleted = True
        self.save()

    def restore(self):
        self.deleted_at = None
        self.is_deleted = False
        self.save()


BOX_FORM_CHOICES = [
    ("NEW", "NEW"),
    ("1F-A", "1F-A"),
    ("1F-B", "1F-B"),
    ("1F-C", "1F-C"),
    ("1F-D", "1F-D"),
    ("2F-A", "2F-A"),
    ("2F-B", "2F-B"),
    ("2F-C", "2F-C"),
    ("2F-D", "2F-D"),
    ("3F-A", "3F-A"),
    ("3F-B", "3F-B"),
    ("3F-C", "3F-C"),
    ("3F-D", "3F-D"),
    ("4F-A", "4F-A"),
    ("4F-B", "4F-B"),
    ("4F-C", "4F-C"),
    ("4F-D", "4F-D"),
]

RACK_VALIDATOR = RegexValidator(
    regex=r'^\d{2}$',
    message="Enter a two digit rack number (01, 02, 11,...)",
    code='invalid_rack'
)


class Storage(SoftDelete, BasicInformation):

    rack = models.CharField(max_length=2, validators=[RACK_VALIDATOR], help_text=RACK_VALIDATOR.message)
    box = models.CharField(choices=BOX_FORM_CHOICES, blank=False, max_length=5)

    history = HistoricalRecords()

    class Meta:
        unique_together = ['rack', 'box']
        ordering = ['rack', 'box']
        verbose_name = "Storage"
        verbose_name_plural = "Storages"

    def count_products_in_box(self):
        return Product.objects.filter(storage=self).count()

    def __str__(self):
        return f'R{self.rack} {self.box}'


DRUG_FORM_CHOICES = [
    ("ampoule", "Ampoule"),
    ("capsules", "Capsules"),
    ("cream", "Cream"),
    ("drink", "Drink"),
    ("drops", "Drops"),
    ("emulsion", "Emulsion"),
    ("gas", "Gas"),
    ("gelhydrogel", "Gel/hydrogel"),
    ("forinh", "For inhalations"),
    ("injections", "Injections"),
    ("lotion", "Lotion"),
    ("pastille", "Pastille"),
    ("paste", "Paste"),
    ("patch", "Patch"),
    ("pills", "Pills"),
    ("powder", "Powder"),
    ("spray", "Spray"),
    ("syrup", "Syrup"),
    ("thinfilms", "Thin films"),
    ("otherderm", "Other/dermal"),
    ("otherext", "Other/external use"),
    ("otherli", "Other/liquid"),
    ("otheror", "Other/oral")
    ]

USAGE_TIME_UNIT_CHOICES = [
    ("days", "Days"),
    ("weeks", "Weeks"),
    ("months", "Months"),
    ("years", "Years")
    ]


class ApprovedDrug(SoftDelete, BasicInformation):
    name = models.CharField(max_length=40)
    is_approved = models.BooleanField(default=True)
    components = models.TextField(max_length=300, null=True, blank=True)
    main_component_dosage = models.CharField(max_length=20)
    label = models.FileField(upload_to='uploads/')
    form = models.CharField(max_length=20, choices=DRUG_FORM_CHOICES)
    usage_time = models.PositiveIntegerField(blank=False)
    usage_time_unit = models.CharField(max_length=20, choices=USAGE_TIME_UNIT_CHOICES, blank=False)

    history = HistoricalRecords()

    class Meta:
        unique_together = ['name', 'main_component_dosage', 'form']
        ordering = ['created_at']
        verbose_name = "Approved drug"
        verbose_name_plural = "Approved drugs"

    def __str__(self):
        if not self.is_approved:
            return f'!NOT APPROVED! {self.name} {self.main_component_dosage}, {self.form} !NOT APPROVED!'
        return f'{self.name} {self.main_component_dosage}, {self.form}'

    def recalculated_usage_time_days(self):
        time_multiplier = {
            "years": 365,
            "months": 30,
            "weeks": 7,
            "days": 1,
        }
        return self.usage_time * time_multiplier.get(self.usage_time_unit, 1)

    def save(self, *args, **kwargs):
        if not self.is_approved:
            self.drug_extra_info = f'DRUG NOT APPROVED FOR USAGE {now().date()}'
        else:
            self.drug_extra_info = ""
        return super(ApprovedDrug, self).save(*args, **kwargs)


QUANTITY_USAGE_CHOICES = [
    ("mg", "MG"),
    ("g", "G"),
    ("ml", "ML"),
    ("pcs", "PCS"),
    ]


class Product(SoftDelete, BasicInformation):
    approved_drug = models.ForeignKey(ApprovedDrug, on_delete=models.DO_NOTHING)
    serial_number = models.CharField(max_length=20)
    quantity = models.PositiveIntegerField(null=False, blank=False)
    quantity_unit = models.CharField(max_length=20, choices=QUANTITY_USAGE_CHOICES)
    storage = models.ForeignKey(Storage, on_delete=models.DO_NOTHING, blank=False)
    best_before_date = models.DateField(blank=False, null=False)
    is_opened = models.BooleanField(default=False, blank=True, null=True)
    opened_date = models.DateField(blank=True, null=True)

    history = HistoricalRecords()

    class Meta:
        unique_together = ['approved_drug', 'serial_number']
        ordering = ['created_at']
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return f"{self.approved_drug}, {self.serial_number}, {self.quantity}{self.quantity_unit}"

    def clean(self, *args, **kwargs):
        if self.is_opened and not self.opened_date:
            raise ValidationError("Please fill in the open date")
        return super().clean()

    def ready_to_use(self):
        product_usable = 'OK'
        product_not_usable = 'DISCARD IMMEDIATELY'

        if self.opened_date and (now().date() - self.opened_date).days > self.approved_drug.recalculated_usage_time_days():
            self.ready_to_use = product_not_usable
        elif self.best_before_date < now().date():
            self.ready_to_use = product_not_usable
        else:
            self.ready_to_use = product_usable
        return self.ready_to_use
