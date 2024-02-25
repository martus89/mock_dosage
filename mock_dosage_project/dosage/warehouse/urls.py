from django.contrib import admin
from django.urls import path
from .views import homepage, login_page, register, users_view, storage_view, approved_drugs_view, product_view

urlpatterns = [
    path('', homepage, name='homepage'),
    path('login', login_page, name='login_page'),
    path('register', register, name='register'),
    path('users', users_view, name='users_view'),
    path('storages', storage_view, name='storage_view'),
    path('approved-drugs', approved_drugs_view, name='approved_drugs_view'),
    path('meds', product_view, name='product_view'),
]
# do a registration and login app