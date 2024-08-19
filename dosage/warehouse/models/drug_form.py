from django.db import models
from .soft_delete import SoftDelete
from .basic_information import BasicInformation
import uuid


class DrugFormChoice(SoftDelete, BasicInformation):
    """
    Different forms of drugs.
    """
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    value = models.CharField(max_length=15, null=False, blank=False, unique=True)
    description = models.CharField(max_length=50, null=False, blank=False)

    class Meta:
        ordering = ['value']
        verbose_name = 'Drug form choice'
        verbose_name_plural = 'Drug form choices'

    def __str__(self):
        return f"{self.value}"
