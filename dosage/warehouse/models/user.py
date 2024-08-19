import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    Group,
)
from django.db import models, transaction


class UserManager(BaseUserManager):
    @transaction.atomic
    def create_user(self, email, password=None, **extra_fields):
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        group = Group.objects.get(name="view_only")
        user.groups.add(group)
        return user

    @transaction.atomic
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        group = Group.objects.get(name="superuser")
        user.groups.add(group)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    email = models.EmailField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname"]

    def __str__(self):
        return self.full_name

    def display_group(self):
        return ", ".join(group.name for group in self.groups.all())

    @property
    def full_name(self):
        return f"{self.name} {self.surname}"
