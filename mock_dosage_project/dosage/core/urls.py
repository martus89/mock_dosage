from django.urls import path
from .views import storage_view, approved_drugs_view, product_view, users_view


urlpatterns = [
    path('storages', storage_view, name='storage_view'),
    path('approved-drugs', approved_drugs_view, name='approved_drugs_view'),
    path('meds', product_view, name='product_view'),
    path('users', users_view, name='users_view'),
]