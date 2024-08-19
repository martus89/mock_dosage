from django.core.validators import MinValueValidator
from django.db import models
from .soft_delete import SoftDelete
from .basic_information import BasicInformation
from .drug_form import DrugFormChoice
import uuid


USAGE_TIME_UNIT_CHOICES = [
    ("days", "Days"),
    ("weeks", "Weeks"),
    ("months", "Months"),
    ("years", "Years"),
]

QUANTITY_USAGE_CHOICES = [
    ("mg", "MG"),
    ("g", "G"),
    ("ml", "ML"),
    ("pcs", "PCS"),
]


class ApprovedDrug(SoftDelete, BasicInformation):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    name = models.CharField(max_length=40)
    is_approved = models.BooleanField(default=True)
    is_controlled = models.BooleanField(default=False)
    components = models.TextField(max_length=300, null=True, blank=True)
    main_component_dosage = models.IntegerField(null=False, blank=False, validators=[MinValueValidator(1)], help_text="Enter a positive value")
    main_component_unit = models.CharField(max_length=20, choices=QUANTITY_USAGE_CHOICES, blank=False)
    label = models.FileField(upload_to='uploads/')
    form = models.ForeignKey(DrugFormChoice, on_delete=models.DO_NOTHING, blank=False)
    usage_time = models.PositiveIntegerField(blank=False, help_text="Enter a positive value")
    usage_time_unit = models.CharField(max_length=20, choices=USAGE_TIME_UNIT_CHOICES, blank=False)
    str_prefix = models.CharField(max_length=30,  default='')

    class Meta:
        unique_together = ['name', 'main_component_dosage', 'form']
        ordering = ['created_at']
        verbose_name = "Approved drug"
        verbose_name_plural = "Approved drugs"

    def __str__(self):
        if not self.str_prefix:
            return f'{self.name} {self.main_component_dosage}, {self.form}'
        return f'{self.str_prefix}{self.name} {self.main_component_dosage}{self.main_component_unit}, {self.form}'

    def recalculated_usage_time_days(self):
        time_multiplier = {
            "years": 365,
            "months": 30,
            "weeks": 7,
            "days": 1,
        }
        return self.usage_time * time_multiplier.get(self.usage_time_unit, 1)
