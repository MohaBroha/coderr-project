from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user account.
    """

    password = serializers.CharField(write_only=True)

    class Meta:
        """
        Metadata configuration for the register serializer.
        """

        model = User
        fields = ["id", "username", "password", "email"]

    def create(self, validated_data):
        """
        Create and return a new user with the validated registration data.
        """
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"],
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
        user = authenticate(username=data["username"], password=data["password"])

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        data["user"] = user
        return data
