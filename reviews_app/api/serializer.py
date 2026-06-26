from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from ..models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
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
    class Meta:
        model = Review
        fields = [
            "business_user",
            "rating",
            "description",
        ]

    def create(self, validated_data):
        return Review.objects.create(
            reviewer=self.context["request"].user,
            **validated_data,
        )

    def validate(self, attrs):
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
    class Meta:
        model = Review
        fields = [
            "rating",
            "description",
        ]
