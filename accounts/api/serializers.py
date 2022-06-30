from django.contrib.auth.password_validation import get_default_password_validators
from django.core.exceptions import ValidationError
from rest_framework import serializers
from ..models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'token']


class RegisterSerializer(UserSerializer):
    password = serializers.CharField()

    class Meta(UserSerializer.Meta):
        fields = ['first_name', 'last_name', 'email', 'password']

    def get_password_errors(self):
        data = self.validated_data.copy()
        password = data.pop('password')
        validators = get_default_password_validators()
        temp_user = User(**data)
        errors = []
        for validator in validators:
            try:
                validator.validate(password, temp_user)
            except ValidationError as e:
                errors.append(str(e))
        return errors


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class ResetPasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField()
    new_password = serializers.CharField()
    confirm_new_password = serializers.CharField()

    def validate(self, data):
        if data.get("new_password") != data.get("confirm_new_password"):
            raise serializers.ValidationError("Passwords do not match")
        return data

    def get_password_errors(self):
        user = self.context.get("user")
        new_password = self.validated_data.get("new_password")
        validators = get_default_password_validators()
        errors = []
        for validator in validators:
            try:
                validator.validate(new_password, user)
            except ValidationError as e:
                errors.append(str(e))
        return errors

