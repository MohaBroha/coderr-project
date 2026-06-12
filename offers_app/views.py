from django.shortcuts import render

from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from .filters import OfferFilter, OfferPagination
from django.db.models import Min


from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Offer
from .serializer import OfferSerializer


class OfferListView(ListAPIView):
    serializer_class = OfferSerializer
    pagination_class = OfferPagination

    queryset = Offer.objects.annotate(
        min_price=Min("details__price"), min_delivery=Min("details__delivery_time")
    )
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_class = OfferFilter
    search_fields = ["title", "description"]
    ordering_fields = ["updated_at", "min_price"]
