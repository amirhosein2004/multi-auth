from django.urls import path
from ..views.auth_views import (
    SendOTPLoginAPIView,
    VerifyOTPLoginAPIView,
    PasswordLoginAPIView,
    SendOTPRegisterAPIView,
    VerifyOTPRegisterAPIView,
    SetPasswordRegisterAPIView,
    LogoutAPIView
)


urlpatterns = [
    # Login flow
    path('login/send-otp/', SendOTPLoginAPIView.as_view(), name='send_otp_login'),
    path('login/verify-otp/', VerifyOTPLoginAPIView.as_view(), name='verify_otp_login'),
    path('login/password/', PasswordLoginAPIView.as_view(), name='password_login'),
    # Register flow
    path('register/send-otp/', SendOTPRegisterAPIView.as_view(), name='send_otp_register'),
    path('register/verify-otp/', VerifyOTPRegisterAPIView.as_view(), name='verify_otp_register'),
    path('register/set-password/', SetPasswordRegisterAPIView.as_view(), name='set_password_register'),    
    # Logout
    path('logout/', LogoutAPIView.as_view(), name='logout'),
]