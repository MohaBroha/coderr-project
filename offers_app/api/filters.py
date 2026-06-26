from django.db.models import Min
import django_filters
from ..models import Offer
from rest_framework.pagination import PageNumberPagination


class OfferFilter(django_filters.FilterSet):
    """
    Filter set for filtering offers by price, delivery time, and creator.
    """

    min_price = django_filters.NumberFilter(method="filter_min_price")
    max_delivery_time = django_filters.NumberFilter(method="filter_max_delivery_time")
    creator_id = django_filters.NumberFilter(field_name="user_id")

    class Meta:
        """
        Metadata configuration for the offer filter.
        """

        model = Offer
        fields = []

    def filter_min_price(self, queryset, name, value):
        """
        Filter offers by the minimum available price.
        """
        return queryset.filter(min_price__gte=value)

    def filter_max_delivery_time(self, queryset, name, value):
        """
        Filter offers by the maximum minimum delivery time.
        """
        return queryset.filter(
            min_delivery_time__lte=value,
        )


class OfferPagination(PageNumberPagination):
    """
    Pagination configuration for offer listings.
    """

    page_size = 6
    page_size_query_param = "page_size"
