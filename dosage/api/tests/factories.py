import string
from datetime import datetime
from random import random
import factory.fuzzy
from warehouse.models import Storage, User, Product, ApprovedDrug
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

# User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker('email')
    name = factory.Faker('first_name')
    surname = factory.Faker('last_name')
    is_active = True
    is_staff = False
    password = factory.PostGenerationMethodCall('set_password', 'defaultpassword')

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        group = Group.objects.get(name="view_only")
        self.groups.add(group)


class SuperUserFactory(UserFactory):
    is_staff = True
    is_superuser = True


class StorageFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Storage

    rack = factory.fuzzy.FuzzyChoice(choices=["01", "02", "03", "04", "05", "06", "07"])
    box = factory.fuzzy.FuzzyChoice(choices=["NEW", "B01", "B03", "B04", "B05", "B06", "B07"])
    created_by = factory.SubFactory(SuperUserFactory)


class ApprovedDrugFactory(factory.Factory):

    class Meta:
        model = ApprovedDrug

    name = factory.fuzzy.FuzzyText(length=8, chars=string.ascii_letters)
    is_approved = factory.fuzzy.FuzzyChoice(choices=[True, True, True, False])
    components = factory.fuzzy.FuzzyText(length=10, chars=string.ascii_letters)
    main_component_dosage = factory.fuzzy.FuzzyInteger(1,99)
    main_component_unit = factory.fuzzy.FuzzyChoice(choices=["µg", "mg", "g", "µL"])
    label = factory.django.ImageField(color="blue", format="JPEG", width=100, height=100)
    form = factory.fuzzy.FuzzyChoice(choices=["ampoule", "drops", "pastille", "spray"])
    usage_time = factory.fuzzy.FuzzyInteger(1, 10)
    usage_time_unit = factory.fuzzy.FuzzyChoice(choices=["days", "weeks", "months", "years"])
    created_by = factory.SubFactory(UserFactory)


def random_opened_date():
    if random.choice([True, False]):
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=10)
        return random.choice([yesterday, today])
    return None


class ProductFactory(factory.Factory):

    class Meta:
        model = Product

    approved_drug = factory.SubFactory(ApprovedDrugFactory)
    serial_number = factory.fuzzy.FuzzyText(length=6, chars=string.ascii_letters)
    quantity = factory.fuzzy.FuzzyInteger(1, 10)
    quantity_unit = factory.fuzzy.FuzzyChoice(choices=["mg", "g", "pcs"])
    storage = factory.SubFactory(StorageFactory)
    best_before_date = factory.Faker('date')
    # best_before_date = factory.fuzzy.FuzzyDate(random_opened_date())
    is_opened = factory.fuzzy.FuzzyChoice(choices=[True, False])
    opened_date = factory.LazyFunction(random_opened_date)
    created_by = factory.SubFactory(UserFactory)
