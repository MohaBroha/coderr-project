from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

from profile_app.models import Profile

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user account.
    """

    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)
    type = serializers.ChoiceField(choices=Profile.USER_TYPE)

    class Meta:
        """
        Metadata configuration for the register serializer.
        """

        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "repeated_password",
            "type",
        ]

    def validate(self, attrs):
        """
        Validate the registration data.
        """
        if attrs["password"] != attrs["repeated_password"]:
            raise serializers.ValidationError({"password": "Passwords do not match."})

        return attrs

    def create(self, validated_data):
        """
        Create a new user and the corresponding profile.
        """
        validated_data.pop("repeated_password")
        user_type = validated_data.pop("type")

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"],
        )

        Profile.objects.create(
            user=user,
            type=user_type,
        )

        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for validating user login credentials.
    """

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Authenticate the user and attach the authenticated user instance
        to the validated data.
        """
        user = authenticate(
            username=data["username"],
            password=data["password"],
        )

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        data["user"] = user
        return data
