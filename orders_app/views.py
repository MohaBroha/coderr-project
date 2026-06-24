from django.db.models import Q

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Order
from .serializer import OrderSerializer


class OrderListView(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        user = self.request.user

        return Order.objects.filter(
            Q(customer_user=user) | Q(business_user=user)
        ).order_by("-updated_at")
