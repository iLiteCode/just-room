from django.urls import path, include
from . import views
from django.contrib.auth.views import (
    LogoutView, 
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

app_name = 'user'

urlpatterns = [
    path('signups/', views.staff_signup, name='staff_signup'),
    path('signins/', views.staff_signin, name='staff_signin'),
    
    # Uncommented and fixed staff_verify_email URL
    path('staff/verify-email/<uidb64>/<token>/', views.staff_verify_email, name='staff_verify_email'),

    # Staff Password Reset
    path('password-resets/', views.StaffCustomPasswordResetView.as_view(), name='staff_password_reset'),
    path('password-resets/done/', PasswordResetDoneView.as_view(template_name='staff_login/staff_password_reset_done.html'), name='staff_password_reset_done'),
    path('password-reset-confirms/<uidb64>/<token>/', views.StaffCustomPasswordResetConfirmView.as_view(), name='staff_password_reset_confirm'),
    path('password-reset-completes/', PasswordResetCompleteView.as_view(template_name='staff_login/staff_password_reset_complete.html'), name='staff_password_reset_complete'),

    # User-related paths (non-staff)
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logout_view, name='logout_view'),
    path('verify_email/<str:uidb64>/<str:token>/', views.verify_email, name='verify_email'),

    # User Password Reset
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='user_login/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(template_name='user_login/password_reset_complete.html'), name='password_reset_complete'),
]