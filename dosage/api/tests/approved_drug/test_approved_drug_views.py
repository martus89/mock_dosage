import pytest
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from api.tests.factories import ApprovedDrugFactory


@pytest.mark.django_db
class TestApprovedDrugViews:
    client = APIClient()

    @pytest.fixture(autouse=True)
    def set_up(self):
        self.client = APIClient()
        self.approveddrug = ApprovedDrugFactory()
        print(self.approveddrug)
        print(self.approveddrug.id)
        print(self.approveddrug.created_by)
        print("SET UP")

    def test_user_can_list_all_approved_drugs(self, superuser, storages):
        self.client.force_authenticate(superuser)
        url = reverse('approved-drug-list')
        response = self.client.get(url)
        assert response.status_code == 200
        assert len(response.json()["results"]) == 3
