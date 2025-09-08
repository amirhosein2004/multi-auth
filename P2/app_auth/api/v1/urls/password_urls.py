from django.urls import path
from ..views.password_views import (
    SendOTPResetPasswordAPIView,
    VerifyOTPResetPasswordAPIView,
    SetNewPasswordAPIView
)


urlpatterns = [
    path('reset-password/send-otp/', SendOTPResetPasswordAPIView.as_view(), name='send_otp_reset_password'),
    path('reset-password/verify-otp/', VerifyOTPResetPasswordAPIView.as_view(), name='verify_otp_reset_password'),
    path('reset-password/set-password/', SetNewPasswordAPIView.as_view(), name='set_new_password'),
]
