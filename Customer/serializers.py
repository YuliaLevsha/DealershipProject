from rest_framework.exceptions import AuthenticationFailed
from Customer.models import Customer
from rest_framework import serializers
from django.contrib.auth import authenticate
from typing import Dict


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = Customer
        fields = ("username", "email", "password", "password2")

    def validate(self, attrs: Dict) -> Dict:
        password = attrs.get("password")
        password2 = attrs.get("password2")
        if password != password2:
            raise serializers.ValidationError("passwords do not match")
        return attrs

    def create(self, validated_data: Dict) -> Customer:
        user = Customer.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            is_active=False,
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    tokens = serializers.DictField(read_only=True)

    def validate(self, attrs: Dict) -> Dict:
        username = attrs.get("username")
        password = attrs.get("password")
        user = authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed("invalid credential try again")
        if not user.is_active:
            raise AuthenticationFailed("Email is not verified")
        tokens = user.tokens
        return {"tokens": tokens}


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=128, write_only=True, required=True)
    confirmation_password = serializers.CharField(
        max_length=128, write_only=True, required=True
    )

    def validate(self, attrs: Dict) -> Dict:
        new_password = attrs.get("new_password")
        confirmation_password = attrs.get("confirmation_password")
        if new_password != confirmation_password:
            raise serializers.ValidationError("passwords do not match")
        return attrs

    def update(self, instance: Customer, validated_data: Dict) -> Customer:
        instance.set_password(validated_data["new_password"])
        instance.save()
        return instance


class ChangePasswordSerializer(ResetPasswordSerializer):
    old_password = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate_old_password(self, old_password: str) -> str:
        user = self.context["request"].user
        if not user.check_password(old_password):
            raise serializers.ValidationError(
                {"old_password": "Old password is not correct"}
            )
        return old_password


class UpdateUsernameEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ("username", "email")
