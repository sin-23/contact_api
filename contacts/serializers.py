from rest_framework import serializers
from .models import Contact
from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

    def validate_email(self, value):
        # Custom email validation logic to support multiple valid formats
        try:
            validate_email(value)
        except DjangoValidationError:
            raise serializers.ValidationError("Invalid email format provided.")
        # Add any additional email format checks if needed
        return value

    def update(self, instance, validated_data):
        request_method = self.context.get('request').method if self.context.get('request') else None

        if request_method == 'PATCH':
            # Only allow updating phone_number and relationship in PATCH requests
            allowed_fields = ['phone_number', 'relationship']
            extra_fields = [field for field in validated_data.keys() if field not in allowed_fields]
            if extra_fields:
                raise serializers.ValidationError(
                    f"PATCH requests can only update {allowed_fields}. You attempted to update: {extra_fields}"
                )
        return super().update(instance, validated_data)
