from django.contrib.auth.models import Group
from django.test import TestCase
from .models import SoftDelete, Storage, ApprovedDrug, Product, User, BasicInformation
from datetime import date
from django.core.exceptions import ValidationError


class UserManagerTestCase(TestCase):
    def setUp(self):
        self.standard_group = Group.objects.create(name='standard_user')
        self.superuser_group = Group.objects.create(name='superuser')

    def test_create_user(self):
        user = User.objects.create_user(email='user@example.com', password='password', name='John', surname='Doe')
        self.assertEqual(user.email, 'user@example.com')
        self.assertTrue(user.check_password('password'))
        self.assertTrue(user.groups.filter(name='standard_user').exists())

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(email='admin@example.com', password='adminpassword', name='Admin', surname='User')
        self.assertEqual(superuser.email, 'admin@example.com')
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.groups.filter(name='superuser').exists())


class UserModelTestCase(TestCase):
    def test_user_string_representation(self):
        user = User.objects.create(email='user@example.com', password='password', name='John', surname='Doe')
        self.assertEqual(str(user), 'Doe_J')

    def test_user_display_group(self):
        standard_group = Group.objects.create(name='standard_user')
        user = User.objects.create(email='user@example.com', password='password', name='John', surname='Doe')
        user.groups.add(standard_group)
        self.assertEqual(user.display_group(), 'standard_user')


class BasicInformationModelTestCase(TestCase):
    def test_basic_information_creation(self):
        user = User.objects.create(email='user@example.com', password='password', name='John', surname='Doe')
        basic_info = BasicInformation.objects.create(created_by=user, extra_info='Test')
        self.assertTrue(basic_info.created_by, user)
        self.assertEqual(basic_info.extra_info, 'Test')


class SoftDeleteModelTestCase(TestCase):
    def test_soft_delete(self):
        soft_delete_instance = SoftDelete.objects.create()
        self.assertFalse(soft_delete_instance.is_deleted)
        soft_delete_instance.delete()
        self.assertTrue(soft_delete_instance.is_deleted)
        soft_delete_instance.restore()
        self.assertFalse(soft_delete_instance.is_deleted)


class StorageModelTestCase(TestCase):
    def test_storage_creation(self):
        storage = Storage.objects.create(rack='01', box='1F-A')
        self.assertEqual(storage.rack, '01')
        self.assertEqual(storage.box, '1F-A')

    def test_storage_str_representation(self):
        storage = Storage.objects.create(rack='01', box='1F-A')
        self.assertEqual(str(storage), 'R01 1F-A')

    def test_unique_together_constraint(self):
        Storage.objects.create(rack='01', box='1F-A')
        with self.assertRaises(Exception):
            Storage.objects.create(rack='01', box='1F-A')  # Should raise an IntegrityError

    def test_invalid_rack_validator(self):
        with self.assertRaises(ValidationError):
            Storage.objects.create(rack='A1', box='1F-A')  # Should raise a ValidationError


class ApprovedDrugModelTestCase(TestCase):
    def test_approved_drug_creation(self):
        approved_drug = ApprovedDrug.objects.create(
            name='Test Drug',
            is_approved=True,
            components='Test Components',
            main_component_dosage='10mg',
            form='capsules',
            usage_time=30,
            usage_time_unit='days'
        )
        self.assertEqual(approved_drug.name, 'Test Drug')
        self.assertTrue(approved_drug.is_approved)

    def test_approved_drug_str_representation(self):
        approved_drug = ApprovedDrug.objects.create(
            name='Test Drug',
            main_component_dosage='10mg',
            form='capsules',
        )
        self.assertEqual(str(approved_drug), 'Test Drug 10mg, capsules')

    def test_recalculated_usage_time_days(self):
        approved_drug = ApprovedDrug.objects.create(
            name='Test Drug',
            usage_time=2,
            usage_time_unit='weeks'
        )
        self.assertEqual(approved_drug.recalculated_usage_time_days(), 14)

    def test_not_approved_drug_extra_info(self):
        approved_drug = ApprovedDrug.objects.create(
            name='Test Drug',
            is_approved=False
        )
        self.assertIn('DRUG NOT APPROVED FOR USAGE', approved_drug.drug_extra_info)


class ProductModelTestCase(TestCase):
    def setUp(self):
        self.approved_drug = ApprovedDrug.objects.create(
            name='Test Drug',
            main_component_dosage='10mg',
            form='capsules',
            usage_time=30,
            usage_time_unit='days'
        )

    def test_product_creation(self):
        product = Product.objects.create(
            approved_drug=self.approved_drug,
            serial_number='123456',
            quantity=10,
            quantity_unit='pcs',
            storage=None,
            best_before_date=date.today()
        )
        self.assertEqual(product.serial_number, '123456')
        self.assertEqual(product.quantity, 10)

    def test_product_ready_to_use(self):
        product = Product.objects.create(
            approved_drug=self.approved_drug,
            serial_number='123456',
            quantity=10,
            quantity_unit='pcs',
            storage=None,
            best_before_date=date.today()
        )
        self.assertEqual(product.ready_to_use(), 'OK')

    def test_invalid_open_date(self):
        product = Product.objects.create(
            approved_drug=self.approved_drug,
            serial_number='123456',
            quantity=10,
            quantity_unit='pcs',
            storage=None,
            best_before_date=date.today(),
            is_opened=True
        )
        with self.assertRaises(ValidationError):
            product.full_clean()
