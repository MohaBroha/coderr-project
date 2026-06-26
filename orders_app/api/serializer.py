from rest_framework import serializers

from ..models import Order
from offers_app.models import OfferDetail
from django.shortcuts import get_object_or_404


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for representing orders.
    """

    delivery_time_in_days = serializers.IntegerField(source="delivery_time")

    class Meta:
        """
        Metadata configuration for the order serializer.
        """

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
    """
    Serializer for creating new orders.
    """

    offer_detail_id = serializers.IntegerField()

    def create(self, validated_data):
        """
        Create a new order from the selected offer detail.
        """
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


class OrderPatchSerializer(serializers.ModelSerializer):
    """
    Serializer for updating the status of an order.
    """

    ALLOWED_STATUS = [
        "in_progress",
        "completed",
        "cancelled",
    ]

    class Meta:
        """
        Metadata configuration for the order patch serializer.
        """

        model = Order
        fields = [
            "status",
        ]

    def validate(self, attrs):
        """
        Validate that only the status field is updated.
        """
        invalid_fields = set(self.initial_data.keys()) - set(self.fields.keys())

        if invalid_fields:
            raise serializers.ValidationError("Only 'status' may be updated.")

        return attrs

    def validate_status(self, value):
        """
        Validate that the provided status is allowed.
        """
        if value not in self.ALLOWED_STATUS:
            raise serializers.ValidationError("Invalid status.")

        return value


class OrderCountSerializer(serializers.Serializer):
    """
    Serializer for returning the number of active orders.
    """

    order_count = serializers.IntegerField()


class CompletedOrderCountSerializer(serializers.Serializer):
    """
    Serializer for returning the number of completed orders.
    """

    completed_order_count = serializers.IntegerField()
