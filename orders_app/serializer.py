from rest_framework import serializers

from .models import Order
from offers_app.models import OfferDetail
from django.shortcuts import get_object_or_404


class OrderSerializer(serializers.ModelSerializer):
    delivery_time_in_days = serializers.IntegerField(source="delivery_time")

    class Meta:
        model = Order
        fields = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "created_at",
            "updated_at",
        ]


class OrderCreateSerializer(serializers.Serializer):
    offer_detail_id = serializers.IntegerField()

    def create(self, validated_data):
        offer_detail_id = validated_data["offer_detail_id"]

        offer_detail = get_object_or_404(
            OfferDetail,
            id=offer_detail_id,
        )

        offer = offer_detail.offer

        order = Order.objects.create(
            customer_user=self.context["request"].user,
            business_user=offer.user,
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time=offer_detail.delivery_time,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type,
            status="in_progress",
        )

        return order
