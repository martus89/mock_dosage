from django.urls import path
from .views import (storage_list, storage_history, approved_drugs_list, product_list, users_view, homepage,
                    view_storage_products, product_history, approved_drugs_history, products_by_approved_drug)


urlpatterns = [
    path('', homepage, name='homepage'),
    path('approved-drugs/', approved_drugs_list, name='approved_drugs_list'),
    path('approved-drugs/<int:pk>/history', approved_drugs_history, name='approved_drugs_history'),
    path('approved-drugs/<int:pk>/products/', products_by_approved_drug, name='products_by_approved_drug'),
    path('storages/', storage_list, name='storage_list'),
    path('storages/<int:pk>/history', storage_history, name='storage_history'),
    path('storages/<int:pk>/products/', view_storage_products, name='view_storage_products'),
    path('products/', product_list, name='product_list'),
    path('products/<int:pk>/history', product_history, name='product_history'),
    path('users/', users_view, name='users_view'),
]