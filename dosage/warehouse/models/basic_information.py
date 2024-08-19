from django.db import models


class BasicInformation(models.Model):
    from .user import User
    created_at = models.DateField(auto_now_add=True, editable=False)
    created_by = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, null=True, blank=True, auto_created=User
    )
    updated_at = models.DateField(auto_now=True, editable=False)
    extra_info = models.TextField(blank=True, default='', null=True)

    class Meta:
        abstract = True
        ordering = ("created_at",)
        verbose_name = "Basic information"
        verbose_name_plural = "Basic information"
