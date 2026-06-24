from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from django_filters.rest_framework import DjangoFilterBackend
from .filters import OfferFilter, OfferPagination
from django.db.models import Min

from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Offer
from .serializer import (
    OfferCreateSerializer,
    OfferSerializer,
    OfferRetrieveSerializer,
    OfferPatchSerializer,
)
from .permissions import IsBusinessUser
from rest_framework.generics import RetrieveUpdateAPIView
from .permissions import IsOfferOwner


class OfferListView(ListCreateAPIView):
    serializer_class = OfferSerializer
    pagination_class = OfferPagination
    permission_classes = [IsBusinessUser]

    queryset = Offer.objects.order_by("-updated_at").annotate(
        min_price=Min("details__price"),
        min_delivery_time=Min("details__delivery_time"),
    )
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_class = OfferFilter
    search_fields = ["title", "description"]
    ordering_fields = ["updated_at", "min_price"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OfferCreateSerializer
        return OfferSerializer

    def perform_create(self, serializer):
        serializer.save()


class OfferDetailView(RetrieveUpdateAPIView):
    serializer_class = OfferRetrieveSerializer

    queryset = Offer.objects.annotate(
        min_price=Min("details__price"),
        min_delivery_time=Min("details__delivery_time"),
    )

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return OfferPatchSerializer
        return OfferRetrieveSerializer

    def get_permissions(self):
        if self.request.method == "PATCH":
            return [
                IsBusinessUser(),
                IsOfferOwner(),
            ]

        return []

    def get_object(self):
        obj = super().get_object()

        if self.request.method == "PATCH":
            self.check_object_permissions(
                self.request,
                obj,
            )

        return obj
