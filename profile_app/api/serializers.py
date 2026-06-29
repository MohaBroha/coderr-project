from rest_framework import serializers
from ..models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for representing and updating user profiles.
    """

    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.CharField(source="user.email")
    user = serializers.IntegerField(source="user.id", read_only=True)

    class Meta:
        """
        Metadata configuration for the profile serializer.
        """

        model = Profile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "location",
            "tel",
            "description",
            "working_hours",
            "type",
            "email",
            "created_at",
        ]
        read_only_fields = ["user", "username", "type", "created_at"]

    def to_representation(self, instance):
        """
        Return the serialized profile with empty strings instead of null values.
        """
        data = super().to_representation(instance)

        fields = [
            "first_name",
            "last_name",
            "location",
            "tel",
            "description",
            "working_hours",
        ]

        for f in fields:
            if data.get(f) is None:
                data[f] = ""

        return data

    def update(self, instance, validated_data):
        """
        Update and return the profile instance.
        """
        user_data = validated_data.pop("user", {})

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if "email" in user_data:
            instance.user.email = user_data["email"]
            instance.user.save()

        instance.save()
        return instance


class ProfileListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing user profiles.
    """

    username = serializers.CharField(source="user.username", read_only=True)
    user = serializers.IntegerField(source="user.id", read_only=True)

    class Meta:
        """
        Metadata configuration for the profile list serializer.
        """

        model = Profile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "location",
            "tel",
            "description",
            "working_hours",
            "type",
        ]
