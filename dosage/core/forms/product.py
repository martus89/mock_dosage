from django import forms
from warehouse.models import Product


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'approved_drug', 'serial_number', 'packaging_quantity', 'packaging_quantity_unit', 'storage', 'best_before_date',
            'is_opened', 'opened_date', 'extra_info'
            ]
        widgets = {'extra_info': forms.Textarea(attrs={'placeholder': 'Optional information'})}


class EditProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'approved_drug', 'serial_number', 'packaging_quantity', 'packaging_quantity_unit', 'storage', 'best_before_date',
            'is_opened', 'opened_date', 'extra_info'
            ]
        widgets = {'extra_info': forms.Textarea(attrs={'placeholder': 'Optional information'})}


class SortingProductForm(forms.Form):

    SORT_CHOICES = [
        ('approved_drug', 'Name'),
        ('serial_number', 'Serial nr'),
        ('packaging_quantity', 'Packaging quantity'),
        ('best_before_date', 'Best before'),
        ('is_opened', 'Opened'),
        ('usage_time', 'Usage time'),
        ('opened_date', 'Opened date'),
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
