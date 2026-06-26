from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from ..models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for representing reviews.
    """

    class Meta:
        """
        Metadata configuration for the review serializer.
        """

        model = Review
        fields = [
            "id",
            "business_user",
            "reviewer",
            "rating",
            "description",
            "created_at",
            "updated_at",
        ]


class ReviewCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new reviews.
    """

    class Meta:
        """
        Metadata configuration for the review creation serializer.
        """

        model = Review
        fields = [
            "business_user",
            "rating",
            "description",
        ]

    def create(self, validated_data):
        """
        Create and return a new review for the authenticated user.
        """
        return Review.objects.create(
            reviewer=self.context["request"].user,
            **validated_data,
        )

    def validate(self, attrs):
        """
        Validate that users cannot review themselves or submit multiple reviews
        for the same business user.
        """
        reviewer = self.context["request"].user
        business_user = attrs["business_user"]

        if reviewer == business_user:
            raise serializers.ValidationError("You cannot review yourself.")

        if Review.objects.filter(
            reviewer=reviewer,
            business_user=business_user,
        ).exists():
            raise PermissionDenied("You have already reviewed this business user.")

        return attrs


class ReviewUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating existing reviews.
    """

    class Meta:
        """
        Metadata configuration for the review update serializer.
        """

        model = Review
        fields = [
            "rating",
            "description",
        ]
