from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import now
from .basic_information import BasicInformation
from .soft_delete import SoftDelete
import uuid
from .approved_drug import ApprovedDrug
from .storage import Storage


QUANTITY_USAGE_CHOICES = [
    ("mg", "MG"),
    ("g", "G"),
    ("ml", "ML"),
    ("pcs", "PCS"),
]

USAGE_TIME_UNIT_CHOICES = [
    ("days", "Days"),
    ("weeks", "Weeks"),
    ("months", "Months"),
    ("years", "Years"),
]


class Product(SoftDelete, BasicInformation):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    approved_drug = models.ForeignKey(ApprovedDrug, on_delete=models.DO_NOTHING)
    serial_number = models.CharField(max_length=20)
    packaging_quantity = models.PositiveIntegerField(null=False, blank=False)
    packaging_quantity_unit = models.CharField(max_length=20, choices=QUANTITY_USAGE_CHOICES)
    storage = models.ForeignKey(Storage, on_delete=models.DO_NOTHING, blank=False)
    best_before_date = models.DateField(blank=False, null=False)
    is_opened = models.BooleanField(default=False, blank=True, null=True)
    opened_date = models.DateField(blank=True, null=True)

    class Meta:
        unique_together = ['approved_drug', 'serial_number']
        ordering = ['created_at']
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return f"{self.approved_drug}, {self.serial_number}, {self.packaging_quantity}{self.packaging_quantity_unit}"

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
