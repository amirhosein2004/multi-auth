import re
from rest_framework import serializers


class PhoneValidationMixin:
    def validate_phone(self, value):
        value = self.normalize_digits(value.strip()) # normalize digits email or phone

        # --- Try phone validation
        phone = self.normalize_phone(value)
        if phone and self.is_valid_iranian_phone(phone):
            return phone

        # --- Neither valid email nor phone
        raise serializers.ValidationError(
            "ورودی نامعتبر است. لطفاً یک شماره تلفن معتبر وارد کنید"
        )

    def normalize_phone(self, phone):
        """
        Normalizes Iranian phone numbers to 09xxxxxxxxx format.
        Supports: +98912..., 0098912..., 98912..., etc.
        """
        phone = re.sub(r'\s+', '', phone)
        phone = phone.replace('+98', '0')
        phone = phone.replace('0098', '0')
        phone = phone.replace('98', '0') if phone.startswith('98') else phone
        return phone
    
    def normalize_digits(self, text: str) -> str:
        """
        Converts Persian and Arabic digits in a string to English digits.
        """
        persian_digits = '۰۱۲۳۴۵۶۷۸۹'
        arabic_digits = '٠١٢٣٤٥٦٧٨٩'
        english_digits = '0123456789'

        translation_table = str.maketrans(
            persian_digits + arabic_digits,
            english_digits * 2
        )
        return text.translate(translation_table)

    def is_valid_iranian_phone(self, phone):
        """
        Checks if the phone number is in valid Iranian mobile format.
        Example: 09123456789
        """
        return re.match(r'^09\d{9}$', phone)


class NationalIdValidationMixin:
    def validate_national_id(self, value):
        """
        Validates Iranian national ID using the official algorithm.
        """
        # Normalize digits (convert Persian/Arabic to English)
        national_id = self.normalize_digits(str(value).strip())
        
        # Check if it's exactly 10 digits
        if not re.match(r'^\d{10}$', national_id):
            raise serializers.ValidationError("کد ملی باید دقیقاً ۱۰ رقم باشد")
        
        # Check for invalid patterns (all same digits)
        if len(set(national_id)) == 1:
            raise serializers.ValidationError("کد ملی نامعتبر است")
        
        # Apply Iranian national ID checksum algorithm
        if not self.is_valid_iranian_national_id(national_id):
            raise serializers.ValidationError("کد ملی وارد شده صحیح نمی‌باشد")
        
        return national_id
    
    def is_valid_iranian_national_id(self, national_id):
        """
        Validates Iranian national ID using the official checksum formula.
        """
        # Convert to list of integers
        digits = [int(d) for d in national_id]
        
        # Calculate checksum
        checksum = 0
        for i in range(9):
            checksum += digits[i] * (10 - i)
        
        remainder = checksum % 11
        check_digit = digits[9]
        
        # Validation rules
        if remainder < 2:
            return check_digit == remainder
        else:
            return check_digit == 11 - remainder
    
    def normalize_digits(self, text: str) -> str:
        """
        Converts Persian and Arabic digits in a string to English digits.
        """
        persian_digits = '۰۱۲۳۴۵۶۷۸۹'
        arabic_digits = '٠١٢٣٤٥٦٧٨٩'
        english_digits = '0123456789'

        translation_table = str.maketrans(
            persian_digits + arabic_digits,
            english_digits * 2
        )
        return text.translate(translation_table)
