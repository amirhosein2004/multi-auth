from rest_framework import serializers
from .mixins import NationalIdValidationMixin
from ....services.auth_services import get_user
from ....services.validation_services import verify_otp
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db import transaction


User = get_user_model()


class SendOTPResetPasswordSerializer(NationalIdValidationMixin, serializers.Serializer):
    """
    Send OTP for reset password
    """
    national_id = serializers.CharField(
        required=True,
        allow_blank=False,
        min_length=10,
        max_length=10,
        error_messages={
            "required": ".کد ملی اجباری است",
            "blank": ".کد ملی اجباری است",
            "max_length": ".کد ملی باید ۱۰ رقم باشد",
            "min_length": ".کد ملی باید ۱۰ رقم باشد",
        },
    )

    def validate(self, attrs):
        """
        Validate user is exists
        """
        national_id = attrs.get("national_id")
        try:
            user = get_user(national_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("کد ملی اشتباه است یا وجود ندارد")

        attrs["user"] = user
        attrs["phone"] = user.phone  
        return attrs


class VerifyOTPResetPasswordSerializer(SendOTPResetPasswordSerializer):
    """
    Verify OTP for reset password
    """
    otp = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=6,
        error_messages={
            "required": ".کد تایید اجباری است",
            "blank": ".کد تایید اجباری است",
            "max_length": ".کد تایید باید ۶ رقم باشد",
        },
    )

    def validate_otp(self, value: str) -> str:
        if not value.isdigit():
            raise serializers.ValidationError(".کد تأیید باید فقط شامل ارقام باشد")
        return value

    def validate(self, attrs):
        """
        Validate OTP for reset password
        """
        attrs = super().validate(attrs)

        valid, error = verify_otp(attrs['phone'], attrs['otp'], "reset_password")
        if error:
            raise serializers.ValidationError({"otp": error})

        return attrs

class SetNewPasswordSerializer(SendOTPResetPasswordSerializer):
    """
    Set new password
    """

    new_password = serializers.CharField(
        required=True, allow_blank=False,
        error_messages={
            'required': '.رمز عبور جدید الزامی است',
            'blank': '.رمز عبور جدید خالی است',
        }
    )
    confirm_password = serializers.CharField(
        required=True, allow_blank=False,
        error_messages={
            'required': '.تایید رمز عبور الزامی است',
            'blank': '.تایید رمز عبور خالی است',
        }
    )

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'detail': '.رمزهای عبور مطابقت ندارند'})
        return attrs

    def save(self):
        with transaction.atomic():
            user = self.validated_data['user']
            user.set_password(self.validated_data['new_password'])
            user.save()
