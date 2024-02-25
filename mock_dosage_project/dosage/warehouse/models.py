from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import now


BOX_FORM_CHOICES = [
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


class Storage(models.Model):
    rack = models.CharField(max_length=3)
    box = models.CharField(choices=BOX_FORM_CHOICES, blank=False, max_length=5)
    extra_info = models.TextField(max_length=250, blank=True)

    class Meta:
        unique_together = ['rack', 'box']
        ordering = ['rack', 'box']

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


class ApprovedDrug(models.Model):
    name = models.CharField(max_length=40)
    is_approved = models.BooleanField(default=True)
    components = models.TextField(max_length=300, null=True, blank=True)
    main_component_dosage = models.CharField(max_length=20)
    label = models.FileField(upload_to='uploads/drug_labels')
    form = models.CharField(max_length=20, choices=DRUG_FORM_CHOICES)
    created_at = models.DateField(auto_now_add=True, editable=False)
    extra_info = models.TextField(max_length=250, blank=True, null=True)
    usage_time = models.PositiveIntegerField(blank=False)
    usage_time_unit = models.CharField(max_length=20, choices=USAGE_TIME_UNIT_CHOICES, blank=False)

    class Meta:
        unique_together = ['name', 'main_component_dosage', 'form']
        ordering = ['name', 'form']

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


class Product(models.Model):
    approved_drug = models.ForeignKey(ApprovedDrug, on_delete=models.DO_NOTHING)
    serial_number = models.CharField(max_length=20)
    quantity = models.PositiveIntegerField(null=False, blank=False)
    quantity_unit = models.CharField(max_length=20, choices=QUANTITY_USAGE_CHOICES)
    storage = models.ForeignKey(Storage, on_delete=models.DO_NOTHING, blank=False)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateField(auto_now_add=True)
    best_before_date = models.DateField(blank=False, null=False)
    is_opened = models.BooleanField(default=False, blank=True, null=True)
    opened_date = models.DateField(blank=True, null=True)
    extra_info = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        unique_together = ['approved_drug', 'serial_number']
        ordering = ['created_at']

    def __str__(self):
        return f"{self.approved_drug}, {self.quantity}{self.quantity_unit}"

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
