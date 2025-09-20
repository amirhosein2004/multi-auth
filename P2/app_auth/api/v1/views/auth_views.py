import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from ....services.auth_services import generate_jwt_tokens_for_user, logout_user, send_otp
from ..serializers.auth_serializers import (
    SendOTPLoginSerializer,
    VerifyOTPLoginSerializer,
    SendOTPRegisterView,
    VerifyOTPRegisterView,
    SetPasswordRegisterView,
    PasswordLoginSerializer,
)
from ....services.cache_services import can_resend, set_resend_cooldown, set_is_verify_phone, get_is_verify_phone
from rest_framework_simplejwt.views import TokenRefreshView


logger = logging.getLogger(__name__)


class SendOTPLoginAPIView(APIView):
    """
    Send OTP for login
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = SendOTPLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']

        can_send, seconds_left = can_resend(phone, "login")
        if not can_send:
            return Response(
                {
                    "detail": f"ثانیه دیگر برای ارسال مجدد صبر کنید {seconds_left % 60} دقیقه و {seconds_left // 60} لطفا ",
                    "cooldown_seconds": seconds_left
                },
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )
        try:
            send_otp(phone, "login")
            set_resend_cooldown(phone, purpose="login", timeout=2 * 60)
            return Response({'detail': 'کد تایید با موفقیت ارسال شد'}, status=status.HTTP_200_OK)  
        except Exception:
            logger.error(f"Login error for {phone}", exc_info=True)
            return Response({'detail': '.خطای غیر منتظره ای رخ داد دوباره تلاش کنید'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyOTPLoginAPIView(APIView):
    """
    Verify OTP and login user
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = VerifyOTPLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            jwt_tokens = generate_jwt_tokens_for_user(serializer.validated_data["user"])  # create JWT token(login)
            return Response({
                'detail': "کاربر با موفقیت وارد شد",
                'access': jwt_tokens['access'],
                'refresh': jwt_tokens['refresh'],
            }, status=status.HTTP_200_OK)  
        except Exception:
            logger.error(f"Login error for {serializer.validated_data['phone']}", exc_info=True)
            return Response({'detail': '.خطای غیر منتظره ای رخ داد دوباره تلاش کنید'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PasswordLoginAPIView(APIView):
    """
    Login user with password
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = PasswordLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data["phone"]

        try:
            jwt_tokens = generate_jwt_tokens_for_user(serializer.validated_data["user"])  # create JWT token(login)
            return Response({
                'detail': "کاربر با موفقیت وارد شد",
                'access': jwt_tokens['access'],
                'refresh': jwt_tokens['refresh'],
            }, status=status.HTTP_200_OK)  
        except Exception:
            logger.error(f"Password login error for {phone}", exc_info=True)
            return Response({'detail': '.خطای غیر منتظره ای رخ داد دوباره تلاش کنید'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class SendOTPRegisterAPIView(APIView):
    """
    Send OTP for register
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = SendOTPRegisterView(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']

        can_send, seconds_left = can_resend(phone, "register")
        if not can_send:
            return Response(
                {
                    "detail": f"ثانیه دیگر برای ارسال مجدد صبر کنید {seconds_left % 60} دقیقه و {seconds_left // 60} لطفا ",
                    "cooldown_seconds": seconds_left
                },
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )
        try:
            send_otp(phone, "register")
            set_resend_cooldown(phone, purpose="register", timeout=2 * 60)
            return Response({'detail': 'کد تایید با موفقیت ارسال شد'}, status=status.HTTP_200_OK)  
        except Exception:
            logger.error(f"Register error for {phone}", exc_info=True)
            return Response({'detail': '.خطای غیر منتظره ای رخ داد دوباره تلاش کنید'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class VerifyOTPRegisterAPIView(APIView):
    """
    Verify OTP for register
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = VerifyOTPRegisterView(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']

        try:
            set_is_verify_phone(phone, "register")
            return Response({'detail': 'کد با موفقیت تایید شد'}, status=status.HTTP_200_OK)  
        except Exception:
            logger.error(f"Register error for {phone}", exc_info=True)
            return Response({'detail': '.خطای غیر منتظره ای رخ داد دوباره تلاش کنید'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class SetPasswordRegisterAPIView(APIView):
    """
    Set password for register and create user
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = SetPasswordRegisterView(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']

        try:
            if get_is_verify_phone(phone, "register"):
                user = serializer.save()
                jwt_tokens = generate_jwt_tokens_for_user(user)  # create JWT token(register)
                return Response({
                    'detail': "کاربر با موفقیت ثبت نام شد",
                    'access': jwt_tokens['access'],
                    'refresh': jwt_tokens['refresh'],
                }, status=status.HTTP_200_OK)  
            else:
                logger.warning(f"user {phone} is not verified")
                return Response({'detail': 'مشکلی پیش آمده لطفا دوباره تلاش کنید'}, status=status.HTTP_400_BAD_REQUEST)  
        except Exception:
            logger.error(f"SetPasswordRegister error for {phone}", exc_info=True)
            return Response({'detail': '.خطای غیر منتظره ای رخ داد دوباره تلاش کنید'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class LogoutAPIView(APIView):
    """logout"""
    permission_classes = []

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh', None)
        
        try:
            logout_user(request.user, refresh_token)
            return Response({'detail': '.با موفقیت خارج شدید'}, status=status.HTTP_205_RESET_CONTENT)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            logger.error(f"Error during logout for user {request.user.id}", exc_info=True)
            return Response({'detail': '.خطای غیر منتظره ای رخ داد دوباره تلاش کنید'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class CustomTokenRefreshView(TokenRefreshView):
    """
    Custom Token Refresh View to refresh access token
    """
