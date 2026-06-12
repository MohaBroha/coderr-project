from rest_framework import serializers
from django.db.models import Min

from .models import Offer, OfferDetail


class OfferDetailSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ["id", "url"]

    def get_url(self, obj):
        return f"/offerdetails/{obj.id}/"


class OfferSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True, read_only=True)

    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            "id",
            "user",
            "title",
            "image",
            "description",
            "created_at",
            "updated_at",
            "details",
            "min_price",
            "min_delivery_time",
            "user_details",
        ]

    def get_min_price(self, obj):
        value = obj.details.aggregate(Min("price"))["price__min"]
        return value if value is not None else 0

    def get_min_delivery_time(self, obj):
        value = obj.details.aggregate(Min("delivery_time"))["delivery_time__min"]
        return value if value is not None else 0

    def get_user_details(self, obj):
        user = obj.user
        return {
            "first_name": user.first_name or "",
            "last_name": user.last_name or "",
            "username": user.username,
        }
