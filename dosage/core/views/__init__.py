from .basic_views import homepage, user_view
from .grouped_views import view_storage_products, view_approved_drug_products, products_by_approved_drug, approved_drug_by_name
from .product import add_product, product_list, edit_product, product_history
from .approved_drug import add_approved_drug, approved_drugs_list, edit_approved_drug, approved_drugs_history
from .storage import add_storage, storage_list, edit_storage, storage_history


__all__ = ['add_product', 'add_storage', 'add_approved_drug', 'homepage', 'user_view', 'storage_list', 'product_list',
           'approved_drugs_list', 'edit_product', 'edit_storage', 'edit_approved_drug', 'view_storage_products',
           'view_approved_drug_products', 'products_by_approved_drug', 'approved_drug_by_name', 'storage_history',
           'product_history', 'approved_drugs_history']
