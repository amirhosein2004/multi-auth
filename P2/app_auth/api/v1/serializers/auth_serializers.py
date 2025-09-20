from rest_framework import serializers
from .mixins import PhoneValidationMixin, NationalIdValidationMixin
from ....services.auth_services import get_user
from ....services.validation_services import verify_otp
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db import transaction


User = get_user_model()


class SendOTPLoginSerializer(NationalIdValidationMixin, serializers.Serializer):
    """
    serializer for send otp login
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


class VerifyOTPLoginSerializer(SendOTPLoginSerializer):
    """
    serializer for verify otp login
    """
    otp = serializers.CharField(
        required=True,
        allow_blank=False,
        min_length=6,
        max_length=6,
        error_messages={
            "required": ".کد تایید اجباری است",
            "blank": ".کد تایید اجباری است",
            "max_length": ".کد تایید باید ۶ رقم باشد",
            "min_length": ".کد تایید باید ۶ رقم باشد",
        },
    )

    def validate_otp(self, value: str) -> str:
        if not value.isdigit():
            raise serializers.ValidationError(".کد تأیید باید فقط شامل ارقام باشد")
        return value

    def validate(self, attrs):
        """
        Validate OTP for login
        """
        attrs = super().validate(attrs)

        valid, error = verify_otp(attrs['phone'], attrs['otp'], "login")
        if error:
            raise serializers.ValidationError({"otp": error})

        return attrs


class PasswordLoginSerializer(SendOTPLoginSerializer):
    """
    Serializer for password-based login
    """
    password = serializers.CharField(
        required=True,
        allow_blank=False,
        write_only=True,
        error_messages={
            "required": ".رمز عبور اجباری است",
            "blank": ".رمز عبور اجباری است",
        },
    )

    def validate(self, attrs):
        """
        Validate user credentials and check if user has password set
        """
        attrs = super().validate(attrs)
        password = attrs.get("password")
        user = attrs['user']

        # Check if user has a password set
        if not user.has_usable_password():
            raise serializers.ValidationError({
                "password": "شما هنوز رمز عبور تنظیم نکرده‌اید. لطفا ابتدا رمز عبور خود را تنظیم کنید"
            })

        # Authenticate user with password
        if not user.check_password(password):
            raise serializers.ValidationError({
                "password": "رمز عبور اشتباه است"
            })

        return attrs


class SendOTPRegisterView(PhoneValidationMixin, NationalIdValidationMixin, serializers.Serializer):
    """
    serializer for send otp register
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
    phone = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=15,
        error_messages={
            "required": ".شماره تلفن اجباری است",
            "blank": ".شماره تلفن اجباری است",
        },
    )

    def validadte(self, attrs):
        """
        Validate user is exists
        """
        national_id = attrs.get("national_id")
        phone = attrs.get("phone")

        if User.objects.filter(phone=phone, username=national_id).exists():
            raise serializers.ValidationError("این کاربر قبلا ثبت شده است")
        
        return attrs


class VerifyOTPRegisterView(SendOTPRegisterView):
    """
    serializer for verify otp register
    """
    otp = serializers.CharField(
        required=True,
        allow_blank=False,
        min_length=6,
        max_length=6,
        error_messages={
            "required": ".کد تایید اجباری است",
            "blank": ".کد تایید اجباری است",
            "max_length": ".کد تایید باید ۶ رقم باشد",
            "min_length": ".کد تایید باید ۶ رقم باشد",
        },
    )

    def validate_otp(self, value: str) -> str:
        if not value.isdigit():
            raise serializers.ValidationError(".کد تأیید باید فقط شامل ارقام باشد")
        return value

    def validate(self, attrs):
        """
        Validate OTP for register
        """
        attrs = super().validate(attrs)

        valid, error = verify_otp(attrs['phone'], attrs['otp'], "register")
        if error:
            raise serializers.ValidationError({"otp": error})

        return attrs


class SetPasswordRegisterView(SendOTPRegisterView):
    """
    serializer for set password
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

    def create(self, validated_data):
        with transaction.atomic():
            national_id = validated_data['national_id']
            phone = validated_data['phone']
            password = validated_data['new_password']

            user = User.objects.create_user(
                username=national_id,
                phone=phone,
                password=password
            )
            return user
