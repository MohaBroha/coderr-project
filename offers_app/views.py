from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from django_filters.rest_framework import DjangoFilterBackend
from .filters import OfferFilter, OfferPagination
from django.db.models import Min

from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Offer
from .serializer import OfferCreateSerializer, OfferSerializer
from .permissions import IsBusinessUser


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
