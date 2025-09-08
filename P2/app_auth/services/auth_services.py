import logging
from django.db import transaction
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from .cache_services import OTPCacheService
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from typing import Any


User = get_user_model()

logger = logging.getLogger(__name__)


def send_otp(phone: str, purpose: str):
    otp_code = OTPCacheService.generate_otp(phone, purpose)
    # TODO: Send OTP to phone
    print(110 * '-' + '\n' + f"OTP Code: {otp_code}" + '\n' + 110 * '-')
    return otp_code



def generate_jwt_tokens_for_user(user: Any) -> dict[str, str]:
    """
    Generate JWT refresh and access tokens for a given user.
    """
    refresh = RefreshToken.for_user(user)
    logger.info(f"Tokens generated for user: {user.id}")
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def logout_user(user, refresh_token: str):
    """
    Handle user logout by blacklisting the refresh token.
    """
    if not refresh_token:
        raise ValidationError({"detail": '.لطفا توکن رفرش را ارسال کنید'})

    try:
        token = RefreshToken(refresh_token) # decode and validate and cnvert to RefreshToken object
        token.blacklist()  # Blacklist the refresh token
        logger.info(f"User {user.id} logged out successfully")
        return True

    except TokenError:
        logger.warning(f"Invalid or expired token for user {user.id}")
        raise ValidationError({"detail": ".توکن نامعتبر یا منقضی است"})


def get_user(national_code : str)-> User:
    """return a user with national code"""
    try:
        return User.objects.get(username=national_code)
    except User.DoesNotExist:
        raise ValidationError({"detail": ".کاربری با این کد ملی وجود ندارد"})
    