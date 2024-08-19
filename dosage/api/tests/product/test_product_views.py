import pytest
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from api.tests.factories import ProductFactory


@pytest.mark.django_db
class TestApprovedDrugViews:
    client = APIClient()

    @pytest.fixture(autouse=True)
    def set_up(self):
        self.client = APIClient()
        self.product = ProductFactory()
        print(self.product)
        print(self.product.id)
        print(self.product.created_by)
        print("SET UP")

    def test_user_can_list_all_products(self, superuser, storages):
        self.client.force_authenticate(superuser)
        url = reverse('product-list')
        response = self.client.get(url)
        assert response.status_code == 200
        assert len(response.json()["results"]) == 3
