from django.urls import path
from django.contrib.auth import views as auth_views
from .views import login_page, registration_form, login_success, logout_page

urlpatterns = [
    path('login', login_page, name='login'),
    path('register', registration_form, name='register'),
    path('login-success', login_success, name='login_success'),
    path('logout', logout_page, name='logout'),
    path('reset-password/', auth_views.PasswordResetView.as_view(template_name='authentication/reset_password.html'), name='reset_password'),
    path('reset-password-sent/', auth_views.PasswordResetDoneView.as_view(template_name='authentication/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='authentication/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='authentication/password_reset_complete.html'), name='password_reset_complete'),
    ]
