from rest_framework import serializers
from django.contrib.auth.models import Group
from django.db import transaction
from warehouse.models import ApprovedDrug, Product, Storage, User, DrugFormChoice


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']
        read_only = []


class ExtendedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = BaseUserSerializer.Meta.fields + ['id', 'name', 'surname', 'is_active', 'is_staff']
        read_only = []


class BaseDrugFormChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrugFormChoice
        fields = ['value']
        read_only = []


class ExtendedDrugFormChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrugFormChoice
        created_by = BaseUserSerializer()
        fields = BaseDrugFormChoiceSerializer.Meta.fields + ['id', 'description', 'created_by', 'created_at', 'extra_info']
        read_only = ['id', 'created_by', 'created_at']


class BaseStorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = ['id', 'rack', 'box']


class ExtendedStorageSerializer(BaseStorageSerializer):
    created_by = ExtendedUserSerializer()

    class Meta(BaseStorageSerializer.Meta):
        model = Storage
        created_by = BaseUserSerializer()
        fields = BaseStorageSerializer.Meta.fields + ['created_at', 'created_by', 'updated_at', 'extra_info']
        read_only = ['id', 'created_at', 'created_by', 'updated_at']


class BaseApprovedDrugSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApprovedDrug
        fields = ['id', 'name', 'main_component_dosage', 'main_component_unit', 'is_approved', 'is_controlled']
        read_only = ['id',]


class ExtendedApprovedDrugSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApprovedDrug
        created_by = BaseUserSerializer()
        form = BaseDrugFormChoiceSerializer()
        fields = BaseApprovedDrugSerializer.Meta.fields + ['components', 'label', 'form', 'usage_time', 'usage_time_unit',
                                                           'created_at', 'created_by', 'updated_at', 'extra_info',]
        read_only = ['id', 'created_at', 'created_by', 'updated_at',]


class BaseProductSerializer(serializers.ModelSerializer):
    approved_drug = BaseApprovedDrugSerializer()
    storage = BaseStorageSerializer()

    class Meta:
        model = Product
        fields = ['id', 'approved_drug', 'serial_number', 'packaging_quantity', 'packaging_quantity_unit', 'storage',
                  'best_before_date', 'is_opened']
        read_only = ['id']


class ExtendedProductSerializer(serializers.ModelSerializer):
    approved_drug = BaseApprovedDrugSerializer()
    created_by = BaseUserSerializer()
    storage = BaseStorageSerializer()

    class Meta:
        model = Product
        fields = BaseProductSerializer.Meta.fields + ['opened_date', 'created_at', 'created_by', 'updated_at', 'extra_info']
        read_only = ['id', 'created_at', 'created_by', 'updated_at',]
