from django import forms
from warehouse.models import Storage


class AddStorageForm(forms.ModelForm):
    class Meta:
        model = Storage
        fields = [
            'rack', 'box', 'extra_info'
            ]
        widgets = {'extra_info': forms.Textarea(attrs={'placeholder': 'Optional information'})}


class EditStorageForm(forms.ModelForm):
    class Meta:
        model = Storage
        fields = ['rack', 'box', 'extra_info']
        widgets = {'extra_info': forms.Textarea(attrs={'placeholder': 'Optional information'})}


class SortingStorageForm(forms.Form):

    SORT_CHOICES = [
        ('rack', 'Rack'),
        ('box', 'Box'),
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
