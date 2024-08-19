from django_filters import rest_framework as filters
from warehouse.models import Storage, User, ApprovedDrug, Product, DrugFormChoice
from django_filters import OrderingFilter


class StorageFilter(filters.FilterSet):
    created_at = filters.DateFilter(field_name='created_at')
    created_by = filters.CharFilter(field_name='created_by')

    o = OrderingFilter(fields={'created_at': 'created_at', 'box': 'box', 'rack': 'rack', 'created_by': 'created_by'},)

    class Meta:
        model = Storage
        fields = ('created_at', 'created_by')


class UserFilter(filters.FilterSet):
    email = filters.CharFilter(field_name='email')
    name = filters.CharFilter(field_name='name')
    surname = filters.CharFilter(field_name='surname')

    o = OrderingFilter(fields={'name': 'name', 'surname': 'surname', 'email': 'email'},)

    class Meta:
        model = User
        fields = ('email', 'name', 'surname')


class ProductFilter(filters.FilterSet):
    created_at = filters.DateFilter(field_name='created_at')
    created_by = filters.CharFilter(field_name='created_by')
    approved_drug = filters.CharFilter(field_name='approved_drug')
    is_opened = filters.BooleanFilter(field_name='is_opened')
    best_before_date = filters.DateFilter(field_name='best_before_date')
    opened_date = filters.DateFilter(field_name='opened_date')
    serial_number = filters.CharFilter(field_name='serial_number')
    storage = filters.CharFilter(field_name='storage')

    o = OrderingFilter(fields={'created_at': 'created_at', 'storage': 'storage', 'created_by': 'created_by', 'best_before_date': 'best_before_date',
                               'opened_date': 'opened_date', 'serial_number': 'serial_number'},)

    class Meta:
        model = Product
        fields = ('created_at', 'created_by', 'approved_drug', 'is_opened', 'best_before_date', 'opened_date', 'serial_number',
                  'storage')


class ApprovedDrugFilter(filters.FilterSet):
    created_at = filters.DateFilter(field_name='created_at')
    created_by = filters.CharFilter(field_name='created_by')
    components = filters.CharFilter(field_name='components')
    is_approved = filters.BooleanFilter(field_name='is_approved')
    form = filters.ModelChoiceFilter(queryset=DrugFormChoice.objects.all(), label='Drug Form', empty_label='All Forms')
    is_controlled = filters.BooleanFilter(field_name='is_controlled')

    o = OrderingFilter(fields={'created_at': 'created_at', 'created_by': 'created_by', 'form': 'form',
                               'main_component_dosage': 'main_component_dosage', 'is_controlled': 'is_controlled'},)

    class Meta:
        model = ApprovedDrug
        fields = ('created_at', 'created_by', 'components', 'is_approved', 'form', 'is_controlled')


class DrugFormFilter(filters.FilterSet):
    value = filters.CharFilter(field_name='value')
    description = filters.CharFilter(field_name='description')
    created_by = filters.CharFilter(field_name='created_by')
    created_at = filters.DateFilter(field_name='created_at')

    o = OrderingFilter(fields={'value': 'value', 'description': 'description', 'created_at': 'created_at',
                               'created_by': 'created_by', 'form': 'form', 'main_component_dosage': 'main_component_dosage',
                               'is_controlled': 'is_controlled'},)

    class Meta:
        model = DrugFormChoice
        fields = ('value', 'created_at', 'created_by')
