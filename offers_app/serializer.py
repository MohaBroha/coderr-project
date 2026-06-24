from rest_framework import serializers
from django.db.models import Min

from .models import Offer, OfferDetail


class OfferDetailSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = [
            "id",
            "url",
            "title",
            "revisions",
            "price",
            "delivery_time",
            "features",
            "offer_type",
        ]

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
        return getattr(obj, "min_price", 0) or 0

    def get_min_delivery_time(self, obj):
        return getattr(obj, "min_delivery_time", 0) or 0

    def get_user_details(self, obj):
        user = obj.user
        return {
            "first_name": user.first_name or "",
            "last_name": user.last_name or "",
            "username": user.username,
        }


class OfferDetailListSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ["id", "url"]

    def get_url(self, obj):
        return f"/offerdetails/{obj.id}/"


class OfferDetailCreateSerializer(serializers.ModelSerializer):
    delivery_time_in_days = serializers.IntegerField(source="delivery_time")

    class Meta:
        model = OfferDetail
        fields = [
            "title",
            "revisions",
            "price",
            "delivery_time_in_days",
            "features",
            "offer_type",
        ]


class OfferCreateSerializer(serializers.ModelSerializer):
    details = OfferDetailCreateSerializer(many=True)

    class Meta:
        model = Offer
        fields = [
            "id",
            "title",
            "image",
            "description",
            "details",
        ]

    def create(self, validated_data):
        details_data = validated_data.pop("details")
        user = self.context["request"].user

        offer = Offer.objects.create(user=user, **validated_data)

        for detail in details_data:
            OfferDetail.objects.create(
                offer=offer,
                title=detail["title"],
                revisions=detail["revisions"],
                price=detail["price"],
                delivery_time=detail["delivery_time"],
                features=detail["features"],
                offer_type=detail["offer_type"],
            )

        return offer


class OfferRetrieveSerializer(serializers.ModelSerializer):
    details = OfferDetailListSerializer(many=True, read_only=True)

    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

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
        ]

    def get_min_price(self, obj):
        return getattr(obj, "min_price", 0) or 0

    def get_min_delivery_time(self, obj):
        return getattr(obj, "min_delivery_time", 0) or 0


class OfferDetailPatchSerializer(serializers.ModelSerializer):
    delivery_time_in_days = serializers.IntegerField(
        source="delivery_time",
        required=False,
    )

    class Meta:
        model = OfferDetail
        fields = [
            "id",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
        ]


class OfferPatchSerializer(serializers.ModelSerializer):
    details = OfferDetailPatchSerializer(
        many=True,
        required=False,
    )

    class Meta:
        model = Offer
        fields = [
            "id",
            "title",
            "image",
            "description",
            "details",
        ]

    def update(self, instance, validated_data):
        details_data = validated_data.pop("details", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if details_data:
            for detail_data in details_data:
                offer_type = detail_data.get("offer_type")

                try:
                    detail = instance.details.get(offer_type=offer_type)
                except OfferDetail.DoesNotExist:
                    continue

                for attr, value in detail_data.items():
                    setattr(detail, attr, value)

                detail.save()

        return instance
