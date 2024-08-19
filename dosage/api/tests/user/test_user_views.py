import pytest
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from api.tests.factories import UserFactory


@pytest.mark.django_db
class TestApprovedDrugViews:
    client = APIClient()

    @pytest.fixture(autouse=True)
    def set_up(self):
        self.client = APIClient()
        self.user = UserFactory()
        print(self.user)
        print(self.user.id)
        print(self.user.email)
        print("SET UP")

    def test_list_all_users(self, superuser, storages):
        self.client.force_authenticate(superuser)
        url = reverse('user-list')
        response = self.client.get(url)
        assert response.status_code == 200
        assert len(response.json()["results"]) == 2


