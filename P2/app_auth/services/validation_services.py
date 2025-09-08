import datetime
import jwt
import logging
from django.conf import settings
from rest_framework.exceptions import ValidationError
from .cache_services import OTPCacheService
from django.core.cache import cache


logger = logging.getLogger(__name__)



def verify_otp(phone: str, code: str, purpose: str) -> tuple[bool, None] | tuple[None, str]:
    """
    Validate OTP for given phone, code, and purpose using cache.

    Returns:
        (True, None) → if OTP is valid
        (None, error_message) → if invalid or expired
    """
    key = OTPCacheService._make_key(phone_number=phone, purpose=purpose)
    real_code = cache.get(key)

    if real_code is None:
        return None, ".کد منقضی شده است. لطفاً دوباره درخواست دهید"
    
    if real_code != code:
        return None, ".کد وارد شده نادرست است"

    cache.delete(key)
    return True, None


def generate_token(
    identity: str,
    token_type: str,
    expires_in_minutes: int = 5,
    extra_payload: dict = None
) -> str:
    """
    Generate a JWT token for various purposes:
    - identity: شناسه کاربر یا هر چیز یکتا
    - token_type: نوع توکن (reset_password, registration, verify_phone, etc.)
    - expires_in_minutes: زمان انقضا توکن
    - extra_payload: اطلاعات اضافی که میخوای داخل payload باشه
    """
    payload = {
        "identity": identity,
        "type": token_type,
        "iat": datetime.datetime.now(datetime.timezone.utc),
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=expires_in_minutes),
    }

    if extra_payload:
        payload.update(extra_payload)

    logger.info(f"{token_type} token generated for {identity}")
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


def decode_token(token: str, expected_type: str = None) -> dict:
    """
    Decode and validate JWT token.
    - expected_type: اگر مشخص شد، نوع توکن حتماً باید با آن مطابقت داشته باشد
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise ValidationError("توکن منقضی شده است")
    except jwt.InvalidTokenError:
        raise ValidationError("توکن نامعتبر است")

    if expected_type and payload.get("type") != expected_type:
        raise ValidationError("نوع توکن نامعتبر است")

    return payload

