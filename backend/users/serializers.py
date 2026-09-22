from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import CustomerProfile, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "name", "email", "role", "date_joined")
        read_only_fields = ("id", "email", "role", "date_joined")


class CustomerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = CustomerProfile
        fields = (
            "id", "user", "phone", "address", "occupation",
            "employment_type", "monthly_income", "created_at",
        )
        read_only_fields = ("id", "user", "created_at")


class ProfileUpdateSerializer(serializers.ModelSerializer):
    """PUT /api/profile/ - the customer may only change name + phone."""

    name = serializers.CharField(max_length=150)

    class Meta:
        model = CustomerProfile
        fields = ("name", "phone", "address", "occupation", "monthly_income")

    def update(self, instance, validated_data):
        name = validated_data.pop("name", None)
        if name:
            instance.user.name = name
            instance.user.save(update_fields=["name"])
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return CustomerProfileSerializer(instance).data


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ("name", "email", "phone", "password", "confirm_password")

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("An account with this email already exists.")
        return value.lower()

    def validate(self, attrs):
        if attrs["password"] != attrs.pop("confirm_password"):
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        phone = validated_data.pop("phone", "")
        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, **validated_data)
        profile, _ = CustomerProfile.objects.get_or_create(user=user)
        if phone:
            profile.phone = phone
            profile.save(update_fields=["phone"])
        # Every new demo customer gets a funded demo account + welcome data.
        from banking.services import bootstrap_customer

        bootstrap_customer(user)
        return user

    def to_representation(self, instance):
        return {"id": instance.id, "name": instance.name, "email": instance.email,
                "role": instance.role}
