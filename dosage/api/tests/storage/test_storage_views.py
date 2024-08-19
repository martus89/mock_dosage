import pytest
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from api.tests.factories import StorageFactory, SuperUserFactory
from warehouse.models import Storage



@pytest.mark.django_db
class TestStorageViews:
    client = APIClient()

    @pytest.fixture(autouse=True)
    def set_up(self):
        self.client = APIClient()
        self.superuser = SuperUserFactory()
        self.storage = StorageFactory(created_by=self.superuser)
        print(self.storage)
        print(self.storage.id)
        print(self.storage.rack)
        print(self.storage.box)
        self.storage_2 = StorageFactory(rack='OLD', box='B1', created_by=self.superuser)
        print(self.storage_2)
        print(self.storage_2.id)
        print(self.storage_2.rack)
        print(self.storage_2.box)
        print("SET UP")

    def test_user_can_list_all_storages(self, superuser):
        self.client.force_authenticate(superuser)
        self.storage = StorageFactory(created_by=superuser)
        url = reverse('storage-list')
        response = self.client.get(url)
        print(Storage.objects.all())
        assert response.status_code == 200
        assert len(response.json()["results"]) == 3

    # def test_user_can_list_own_storages(self, regular_user):
    #     self.client.force_authenticate(regular_user)
    #     url = reverse('storage-list')
    #     response = self.client.get(url)
    #     assert response.status_code == 200
    #     assert len(response.json()["results"]) == 2
    #
    # def test_total_new_rack_count(self, superuser):
    #     self.client.force_authenticate(superuser)
    #     url = reverse('storage-total-new-rack-count')
    #     response = self.client.get(url)
    #     assert response.status_code == 200
    #     assert response.json() == 2
