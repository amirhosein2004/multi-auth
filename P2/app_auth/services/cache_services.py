from django.core.cache import cache
import secrets
import logging


logger = logging.getLogger(__name__)


class OTPCacheService:
    """
    Service class for generating and storing OTP codes in cache.
    Used for phone verification (e.g., login, registration, reset paasword).
    """
    OTP_TTL = 2 * 60  # 2 minutes in seconds

    @staticmethod
    def _make_key(phone_number=None, purpose=None):
        """
        Generates a unique cache key for the given phone and purpose.
        """
        phone = phone_number
        return f"otp:{purpose}"

    @classmethod
    def generate_otp(cls, phone_number=None, purpose="login"):
        """
        Generates a 6-digit OTP, stores it in cache for a limited time, and returns it.
        Args:
            phone_number (str): User's phone number (optional)
            purpose (str): OTP purpose (e.g., "login", "register")
        Returns:
            str: The generated OTP code
        """
        otp = str(secrets.randbelow(1000000)).zfill(6)
        key = cls._make_key(phone_number, purpose)
        cache.set(key, otp, timeout=cls.OTP_TTL)
        logger.info(f"Generated OTP for {phone_number} (purpose: {purpose})")
        return otp


def set_is_verify_phone(phone: str, purpose: str, timeout: int = 60 * 10):
    """
    Set a cache key for is_verify_phone
    """
    cache.set(f"is_verify_{phone}_{purpose}", True, timeout=timeout)

def get_is_verify_phone(phone: str, purpose: str) -> bool:
    """
    Get a cache key for is_verify_phone
    if exist return True and delete cache else return False
    """
    if cache.get(f"is_verify_{phone}_{purpose}"):
        cache.delete(f"is_verify_{phone}_{purpose}")
        return True
    return False


def get_resend_cache_key(phone: str, purpose: str) -> str:
    """
    Generate a cache key for resend cooldown tracking based on the user's phone and purpose.
    """
    return f"resend_{phone}_{purpose}"

def can_resend(phone: str, purpose: str) -> tuple[bool, int]:
    """
    Check if a resend (OTP or confirmation link) is allowed for the given phone and purpose.
    
    Returns:
        (bool, int): 
            - True if resend is allowed, False otherwise.
            - Seconds remaining until next allowed resend.
    """
    cache_key = get_resend_cache_key(phone, purpose)
    seconds_left = cache.ttl(cache_key)
    if seconds_left and seconds_left > 0:
        return False, seconds_left
    return True, 0

def set_resend_cooldown(phone: str, purpose: str, timeout: int = 300) -> None:
    """
    Set a cooldown period for resending OTP or confirmation link.
    
    Args:
        phone (str): The target phone number.
        purpose (str): The purpose of the resend (e.g., "login", "register", "reset_password").
        timeout (int): Cooldown time in seconds.
    """
    cache_key = get_resend_cache_key(phone, purpose)
    cache.set(cache_key, True, timeout=timeout)
