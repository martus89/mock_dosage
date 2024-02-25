from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Product, ApprovedDrug, Storage, BOX_FORM_CHOICES, USAGE_TIME_UNIT_CHOICES, DRUG_FORM_CHOICES
from django.contrib.auth.models import User
from django.utils.timezone import now


class StorageModels(TestCase):

    def test_valid_choices(self):
        valid_choices = [choice[0] for choice in BOX_FORM_CHOICES]

        for choice in valid_choices:
            storage = Storage(rack="01", box=choice)
            storage.full_clean()

    def test_invalid_choices(self):
        invalid_choice = "Invalid-Choice"
        with self.assertRaises(ValueError):
            storage = Storage(rack="01", box=invalid_choice)
            storage.full_clean()

    def test_unique_together(self):
        storage1 = Storage(rack="01", box="1F-A")
        storage1.full_clean()
        storage1.save()

        storage2 = Storage(rack="01", box="1F-A")
        with self.assertRaises(Exception):
            storage2.full_clean()
            storage2.save()

    def test_str_method(self):
        storage = Storage(rack="01", box="1F-A")
        self.assertEqual(str(storage), 'R01 1F-A')


class ApprovedDrugModelTest(TestCase):
    def setUp(self):
        self.label_file = SimpleUploadedFile(
            "label.txt", b"file_content", content_type="text/plain"
        )

    def test_str_method(self):
        drug = ApprovedDrug(
            name="Test Drug",
            is_approved=True,
            components="Component A, Component B",
            main_component_dosage="10mg",
            label=self.label_file,
            form="capsules",
            usage_time=30,
            usage_time_unit="days",
        )
        self.assertEqual(
            str(drug), "Test Drug 10mg, capsules"
        )

    def test_recalculated_usage_time_days_method(self):
        drug = ApprovedDrug(
            name="Test Drug",
            is_approved=True,
            components="Component A, Component B",
            main_component_dosage="10mg",
            label=self.label_file,
            form="capsules",
            usage_time=2,
            usage_time_unit="weeks",
        )
        self.assertEqual(drug.recalculated_usage_time_days(), 14)

    def test_not_approved_extra_info(self):
        not_approved_drug = ApprovedDrug(
            name="Not Approved Drug",
            is_approved=False,
            components="Component A, Component B",
            main_component_dosage="10mg",
            label=self.label_file,
            form="capsules",
            usage_time=30,
            usage_time_unit="days",
        )
        not_approved_drug.save()
        self.assertEqual(
            not_approved_drug.drug_extra_info,
            f"DRUG NOT APPROVED FOR USAGE {now().date()}",
        )

    def test_approved_extra_info(self):
        approved_drug = ApprovedDrug(
            name="Approved Drug",
            is_approved=True,
            components="Component A, Component B",
            main_component_dosage="10mg",
            label=self.label_file,
            form="capsules",
            usage_time=30,
            usage_time_unit="days",
        )
        approved_drug.save()
        self.assertEqual(approved_drug.drug_extra_info, "")

    def test_unique_together(self):
        drug1 = ApprovedDrug(
            name="Test Drug",
            is_approved=True,
            components="Component A, Component B",
            main_component_dosage="10mg",
            label=self.label_file,
            form="capsules",
            usage_time=30,
            usage_time_unit="days",
        )
        drug1.save()

        drug2 = ApprovedDrug(
            name="Test Drug",
            is_approved=True,
            components="Component C, Component D",
            main_component_dosage="20mg",
            label=self.label_file,
            form="capsules",
            usage_time=60,
            usage_time_unit="days",
        )
        with self.assertRaises(Exception):
            drug2.save()


class ProductModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.storage = Storage.objects.create(rack="01", box="1F-A")
        self.approved_drug = ApprovedDrug.objects.create(
            name="Test Drug",
            is_approved=True,
            components="Component A, Component B",
            main_component_dosage="10mg",
            label=None,
            form="capsules",
            usage_time=30,
            usage_time_unit="days",
        )

    def test_str_method(self):
        product = Product(
            approved_drug=self.approved_drug,
            serial_number="SN123",
            quantity=50,
            quantity_unit="mg",
            storage=self.storage,
            created_by=self.user,
            best_before_date=timezone.now().date(),
        )
        self.assertEqual(
            str(product), "Test Drug 10mg, capsules, 50mg"
        )

    def test_clean_method_opened_date_missing(self):
        product = Product(
            approved_drug=self.approved_drug,
            serial_number="SN123",
            quantity=50,
            quantity_unit="mg",
            storage=self.storage,
            created_by=self.user,
            best_before_date=timezone.now().date(),
            is_opened=True,
        )
        with self.assertRaises(ValidationError):
            product.clean()

    def test_clean_method_opened_date_present(self):
        product = Product(
            approved_drug=self.approved_drug,
            serial_number="SN123",
            quantity=50,
            quantity_unit="mg",
            storage=self.storage,
            created_by=self.user,
            best_before_date=timezone.now().date(),
            is_opened=True,
            opened_date=timezone.now().date(),
        )
        try:
            product.clean()
        except ValidationError:
            self.fail("clean() method should not raise ValidationError when opened_date is present.")

    def test_ready_to_use_method_usable(self):
        product = Product(
            approved_drug=self.approved_drug,
            serial_number="SN123",
            quantity=50,
            quantity_unit="mg",
            storage=self.storage,
            created_by=self.user,
            best_before_date=timezone.now().date() + timezone.timedelta(days=10),
            is_opened=False,
        )
        self.assertEqual(product.ready_to_use(), "OK")

    def test_ready_to_use_method_not_usable_due_to_opened_date(self):
        product = Product(
            approved_drug=self.approved_drug,
            serial_number="SN123",
            quantity=50,
            quantity_unit="mg",
            storage=self.storage,
            created_by=self.user,
            best_before_date=timezone.now().date(),
            is_opened=True,
            opened_date=timezone.now().date() - timezone.timedelta(days=31),
        )
        self.assertEqual(product.ready_to_use(), "DISCARD IMMEDIATELY")

    def test_ready_to_use_method_not_usable_due_to_best_before_date(self):
        product = Product(
            approved_drug=self.approved_drug,
            serial_number="SN123",
            quantity=50,
            quantity_unit="mg",
            storage=self.storage,
            created_by=self.user,
            best_before_date=timezone.now().date() - timezone.timedelta(days=1),
            is_opened=False,
        )
        self.assertEqual(product.ready_to_use(), "DISCARD IMMEDIATELY")
