from django.contrib.auth import views as auth_views
from django.urls import path
from .views import registration_form, login_success

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='authentication/login.html'), name='login'),
    path('register/', registration_form, name='register'),
    path('login-success/', login_success, name='login_success'),
    path('logout/', auth_views.LogoutView.as_view(template_name='authentication/logout.html'), name='logout'),
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='authentication/change_password.html'), name='change_password'),
    path('change-password-done/', auth_views.PasswordChangeDoneView.as_view(template_name='authentication/change_password_done.html'), name='password_change_done'),
    path('reset-password/', auth_views.PasswordResetView.as_view(template_name='authentication/reset_password.html'), name='reset_password'),
    path('reset-password-sent/', auth_views.PasswordResetDoneView.as_view(template_name='authentication/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='authentication/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='authentication/password_reset_complete.html'), name='password_reset_complete'),
    ]
