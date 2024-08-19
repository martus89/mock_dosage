from django import forms
from warehouse.models import ApprovedDrug


class AddApprovedDrugForm(forms.ModelForm):
    class Meta:
        model = ApprovedDrug
        fields = [
            'name', 'is_approved', 'is_controlled', 'components', 'main_component_dosage', 'main_component_unit',
            'label', 'form', 'usage_time', 'usage_time_unit', 'extra_info'
            ]
        widgets = {'extra_info': forms.Textarea(attrs={'placeholder': 'Optional information'})}


class EditApprovedDrugForm(forms.ModelForm):
    class Meta:
        model = ApprovedDrug
        fields = [
            'name', 'is_approved', 'is_controlled', 'components', 'main_component_dosage', 'main_component_unit',
            'label', 'form', 'usage_time', 'usage_time_unit', 'extra_info'
            ]
        widgets = {'extra_info': forms.Textarea(attrs={'placeholder': 'Optional information'})}


class SortingApprovedDrugForm(forms.Form):

    SORT_CHOICES = [
        ('name', 'Name'),
        ('is_approved', 'Approved'),
        ('is_controlled', 'Controlled'),
        ('main_component_dosage', 'Main component'),
        ('form', 'Form'),
        ('usage_time', 'Usage time'),
        ('created_by', 'Created by'),
        ('created_at', 'Created at'),
        ('updated_at', 'Updated at'),
    ]

    ORDER_CHOICES = [
        ('asc', 'Ascending'),
        ('desc', 'Descending'),
    ]

    sort_by = forms.ChoiceField(choices=SORT_CHOICES, required=False, label='Sort By')
    order = forms.ChoiceField(choices=ORDER_CHOICES, required=False, label='Order')
