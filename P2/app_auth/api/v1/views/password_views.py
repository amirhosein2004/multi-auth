import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..serializers.password_serializers import (
    SendOTPResetPasswordSerializer,
    VerifyOTPResetPasswordSerializer,
    SetNewPasswordSerializer
)
from ....services.auth_services import send_otp
from ....services.cache_services import can_resend, set_resend_cooldown, set_is_verify_phone, get_is_verify_phone


logger = logging.getLogger(__name__)


class SendOTPResetPasswordAPIView(APIView):
    """
    Send OTP for reset password
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = SendOTPResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']

        can_send, seconds_left = can_resend(phone, "reset_password")
        if not can_send:
            return Response(
                {
                    "detail": f"ثانیه دیگر برای ارسال مجدد صبر کنید {seconds_left % 60} دقیقه و {seconds_left // 60} لطفا ",
                    "cooldown_seconds": seconds_left
                },
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )
        try:
            send_otp(phone, "reset_password")
            set_resend_cooldown(phone, purpose="reset_password", timeout=2 * 60)
            return Response({'detail': 'کد تایید با موفقیت ارسال شد'}, status=status.HTTP_200_OK)  
        except Exception:
            logger.error(f"Reset password error for {phone}", exc_info=True)
            return Response({'detail': '.خطای غیر منتظره ای رخ داد دوباره تلاش کنید'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class VerifyOTPResetPasswordAPIView(APIView):
    """
    Verify OTP for reset password
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = VerifyOTPResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']

        try:
            set_is_verify_phone(phone, "reset_password")
            return Response({'detail': 'کد با موفقیت تایید شد'}, status=status.HTTP_200_OK)  
        except Exception:
            logger.error(f"Register error for {phone}", exc_info=True)
            return Response({'detail': '.خطای غیر منتظره ای رخ داد دوباره تلاش کنید'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class SetNewPasswordAPIView(APIView):
    """
    Set new password
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = SetNewPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']

        try:
            if get_is_verify_phone(phone, "reset_password"):
                serializer.save()
                return Response({'detail': 'رمز جدید با موفقیت ثبت شد'}, status=status.HTTP_200_OK)  
            else:
                logger.warning(f"user {phone} is not verified")
                return Response({'detail': 'مشکلی پیش آمده لطفا دوباره تلاش کنید'}, status=status.HTTP_400_BAD_REQUEST)  
        except Exception:
            logger.error(f"SetPasswordRegister error for {phone}", exc_info=True)
            return Response({'detail': '.خطای غیر منتظره ای رخ داد دوباره تلاش کنید'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
