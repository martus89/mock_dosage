from django.db import models
from django.utils import timezone


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

    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.is_deleted = True
        self.save()

    def restore(self):
        self.deleted_at = None
        self.is_deleted = False
        self.save()
