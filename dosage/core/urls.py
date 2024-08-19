from django.urls import path
from core.views.basic_views import (user_view, homepage)
from core.views.grouped_views import (view_storage_products, products_by_approved_drug, approved_drug_by_name)
from core.views.approved_drug import (approved_drugs_list, add_approved_drug, edit_approved_drug, approved_drugs_history)
from core.views.storage import (storage_list, add_storage, edit_storage, storage_history)
from core.views.product import (product_list, add_product, edit_product, product_history)
from core.views.search_view import search


urlpatterns = [

    # Base views
    path('', homepage, name='homepage'),
    path('user/', user_view, name='user_view'),
    path('search/', search, name='search_result'),


    # Approved drugs views
    path('approved-drug/', approved_drugs_list, name='approved_drugs_list'),
    path('approved-drug/add', add_approved_drug, name='add_approved_drug'),
    path('approved-drug/<uuid:pk>/edit', edit_approved_drug, name='edit_approved_drug'),
    path('approved-drug/<uuid:pk>/history', approved_drugs_history, name='approved_drugs_history'),
    path('approved-drug/<uuid:pk>/products/', products_by_approved_drug, name='products_by_approved_drug'),
    path('approved-drug/<str:name>/', approved_drug_by_name, name='approved_drug_by_name'),


    # Storage views
    path('storage/', storage_list, name='storage_list'),
    path('storage/add', add_storage, name='add_storage'),
    path('storage/<uuid:pk>/edit', edit_storage, name='edit_storage'),
    path('storage/<uuid:pk>/history', storage_history, name='storage_history'),
    path('storage/<uuid:pk>/products/', view_storage_products, name='view_storage_products'),


    # Product views
    path('product/', product_list, name='product_list'),
    path('product/add', add_product, name='add_product'),
    path('product/<uuid:pk>/edit', edit_product, name='edit_product'),
    path('product/<uuid:pk>/history', product_history, name='product_history'),
]
