from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from django_filters.rest_framework import DjangoFilterBackend
from .filters import OfferFilter, OfferPagination
from django.db.models import Min

from rest_framework.filters import SearchFilter, OrderingFilter

from ..models import Offer, OfferDetail
from .serializer import (
    OfferCreateSerializer,
    OfferSerializer,
    OfferRetrieveSerializer,
    OfferPatchSerializer,
    OfferDetailRetrieveSerializer,
)
from .permissions import IsBusinessUser
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .permissions import IsOfferOwner
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated


class OfferListView(ListCreateAPIView):
    """
    API view for listing and creating offers.
    """

    serializer_class = OfferSerializer
    pagination_class = OfferPagination

    queryset = Offer.objects.order_by("-updated_at").annotate(
        min_price=Min("details__price"),
        min_delivery_time=Min("details__delivery_time"),
    )
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_class = OfferFilter
    search_fields = ["title", "description"]
    ordering_fields = ["updated_at", "min_price"]

    def get_permissions(self):
        """
        Return the permissions required for the current request.
        """
        if self.request.method == "POST":
            return [IsBusinessUser()]

        return []

    def get_serializer_class(self):
        """
        Return the serializer class for the current request.
        """
        if self.request.method == "POST":
            return OfferCreateSerializer
        return OfferSerializer

    def perform_create(self, serializer):
        """
        Save a newly created offer.
        """
        serializer.save()


class OfferDetailView(RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting offers.
    """

    serializer_class = OfferRetrieveSerializer

    queryset = Offer.objects.annotate(
        min_price=Min("details__price"),
        min_delivery_time=Min("details__delivery_time"),
    )

    def get_serializer_class(self):
        """
        Return the serializer class for the current request.
        """
        if self.request.method == "PATCH":
            return OfferPatchSerializer
        return OfferRetrieveSerializer

    def get_permissions(self):
        """
        Return the permissions required for the current request.
        """
        if self.request.method == "GET":
            return [IsAuthenticated()]

        if self.request.method in ["PATCH", "DELETE"]:
            return [
                IsBusinessUser(),
                IsOfferOwner(),
            ]

        return []

    def get_object(self):
        """
        Retrieve the requested offer and check object permissions when required.
        """
        obj = super().get_object()

        if self.request.method in ["PATCH", "DELETE"]:
            self.check_object_permissions(
                self.request,
                obj,
            )

        return obj


class OfferDetailRetrieveView(RetrieveAPIView):
    """
    API view for retrieving a single offer detail.
    """

    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailRetrieveSerializer
    permission_classes = [IsAuthenticated]
