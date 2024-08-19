from django.core.validators import RegexValidator
from django.db import models
from .soft_delete import SoftDelete
from .user import User
from .basic_information import BasicInformation
import uuid


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
    regex=r"^\d{2}$",
    message="Enter a two digit rack number (01, 02, 11,...)",
    code="invalid_rack",
)


class Storage(SoftDelete, BasicInformation):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rack = models.CharField(
        max_length=2, validators=[RACK_VALIDATOR], help_text=RACK_VALIDATOR.message
    )
    box = models.CharField(choices=BOX_FORM_CHOICES, blank=False, max_length=5)
    updated_by = models.ForeignKey(User, related_name='basic_informations_updated_by', on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta:
        unique_together = ["rack", "box"]
        ordering = ["rack", "box"]
        verbose_name = "Storage"
        verbose_name_plural = "Storages"

    def count_products_in_box(self):
        from .product import Product
        return Product.objects.filter(storage=self).count()

    def __str__(self):
        return f"R{self.rack} B{self.box}"

    # def get_absolute_url(self):
    #     return reverse('storage_list', args=[str(self.id)])
