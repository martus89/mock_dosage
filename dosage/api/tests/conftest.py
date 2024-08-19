import pytest
from rest_framework.test import APIClient
from warehouse.models import Storage
from django.contrib.auth import get_user_model
from api.tests.factories import StorageFactory

User = get_user_model()


@pytest.fixture
def client():
	return APIClient()


@pytest.fixture
def superuser(client):
	return User.objects.create_superuser(email='admin@example.com', password='password', name='Super', surname='User')


@pytest.fixture
def regular_user(client):
	return User.objects.create_user(email='user@example.com', password='password', name='Regular', surname='User')


@pytest.fixture
def storages(regular_user, client, superuser):
	StorageFactory(rack='NEW', box='A1', created_by=regular_user)
	StorageFactory(rack='OLD', box='B1', created_by=regular_user)
	StorageFactory(rack='NEW', box='C1', created_by=superuser)
