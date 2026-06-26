from rest_framework import serializers

from ..models import Offer, OfferDetail


class OfferDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for representing offer details.
    """

    url = serializers.SerializerMethodField()

    class Meta:
        """
        Metadata configuration for the offer detail serializer.
        """

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
        """
        Return the relative URL of the offer detail.
        """
        return f"/offerdetails/{obj.id}/"


class OfferSerializer(serializers.ModelSerializer):
    """
    Serializer for representing offers with related details.
    """

    details = OfferDetailSerializer(many=True, read_only=True)

    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()

    class Meta:
        """
        Metadata configuration for the offer serializer.
        """

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
        """
        Return the minimum price of the offer.
        """
        return getattr(obj, "min_price", 0) or 0

    def get_min_delivery_time(self, obj):
        """
        Return the minimum delivery time of the offer.
        """
        return getattr(obj, "min_delivery_time", 0) or 0

    def get_user_details(self, obj):
        """
        Return basic information about the offer owner.
        """
        user = obj.user
        return {
            "first_name": user.first_name or "",
            "last_name": user.last_name or "",
            "username": user.username,
        }


class OfferDetailListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing offer detail URLs.
    """

    url = serializers.SerializerMethodField()

    class Meta:
        """
        Metadata configuration for the offer detail list serializer.
        """

        model = OfferDetail
        fields = ["id", "url"]

    def get_url(self, obj):
        """
        Return the relative URL of the offer detail.
        """
        return f"/offerdetails/{obj.id}/"


class OfferDetailAbsoluteUrlSerializer(serializers.ModelSerializer):
    """
    Serializer for representing offer details with absolute URLs.
    """

    url = serializers.SerializerMethodField()

    class Meta:
        """
        Metadata configuration for the offer detail absolute URL serializer.
        """

        model = OfferDetail
        fields = [
            "id",
            "url",
        ]

    def get_url(self, obj):
        """
        Return the absolute URL of the offer detail.
        """
        request = self.context.get("request")

        return request.build_absolute_uri(f"/api/offerdetails/{obj.id}/")


class OfferDetailCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating offer details.
    """

    delivery_time_in_days = serializers.IntegerField(source="delivery_time")

    class Meta:
        """
        Metadata configuration for the offer detail creation serializer.
        """

        model = OfferDetail
        fields = [
            "id",
            "title",
            "revisions",
            "price",
            "delivery_time_in_days",
            "features",
            "offer_type",
        ]


class OfferCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating offers with their related details.
    """

    details = OfferDetailCreateSerializer(many=True)

    class Meta:
        """
        Metadata configuration for the offer creation serializer.
        """

        model = Offer
        fields = [
            "id",
            "title",
            "image",
            "description",
            "details",
        ]

    def create(self, validated_data):
        """
        Create an offer together with its associated offer details.
        """
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

    def validate_details(self, value):
        """
        Validate that exactly three offer details are provided.
        """
        if len(value) != 3:
            raise serializers.ValidationError(
                "An offer must contain exactly 3 details."
            )
        return value


class OfferRetrieveSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving offers with absolute detail URLs.
    """

    details = OfferDetailAbsoluteUrlSerializer(
        many=True,
        read_only=True,
    )
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

    class Meta:
        """
        Metadata configuration for the offer retrieve serializer.
        """

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
        """
        Return the minimum price of the offer.
        """
        return getattr(obj, "min_price", 0) or 0

    def get_min_delivery_time(self, obj):
        """
        Return the minimum delivery time of the offer.
        """
        return getattr(obj, "min_delivery_time", 0) or 0


class OfferDetailPatchSerializer(serializers.ModelSerializer):
    """
    Serializer for partially updating offer details.
    """

    delivery_time_in_days = serializers.IntegerField(
        source="delivery_time",
        required=False,
    )

    class Meta:
        """
        Metadata configuration for the offer detail patch serializer.
        """

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
    """
    Serializer for partially updating offers and their details.
    """

    details = OfferDetailPatchSerializer(
        many=True,
        required=False,
    )

    class Meta:
        """
        Metadata configuration for the offer patch serializer.
        """

        model = Offer
        fields = [
            "id",
            "title",
            "image",
            "description",
            "details",
        ]

    def update(self, instance, validated_data):
        """
        Update an offer and its associated offer details.
        """
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


class OfferDetailRetrieveSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving offer detail information.
    """

    delivery_time_in_days = serializers.IntegerField(source="delivery_time")

    class Meta:
        """
        Metadata configuration for the offer detail retrieve serializer.
        """

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
