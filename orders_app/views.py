from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated

from .models import Order
from .serializer import (
    OrderPatchSerializer,
    OrderSerializer,
    OrderCreateSerializer,
    OrderCountSerializer,
)

from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .permissions import (
    IsBusinessUser,
    IsCustomerUser,
    IsOrderBusinessOwner,
    IsStaffUser,
)


class OrderListView(ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsCustomerUser]
    pagination_class = None

    def get_queryset(self):
        user = self.request.user

        return Order.objects.filter(
            Q(customer_user=user) | Q(business_user=user)
        ).order_by("-updated_at")

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OrderCreateSerializer

        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        order = serializer.save()

        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED,
        )

    def get_permissions(self):
        if self.request.method == "POST":
            return [
                IsCustomerUser(),
            ]

        return [
            IsAuthenticated(),
        ]


class OrderDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderPatchSerializer

    def get_permissions(self):
        if self.request.method == "PATCH":
            return [
                IsBusinessUser(),
                IsOrderBusinessOwner(),
            ]

        if self.request.method == "DELETE":
            return [
                IsStaffUser(),
            ]

        return []

    def get_object(self):
        obj = super().get_object()

        self.check_object_permissions(
            self.request,
            obj,
        )

        return obj

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop(
            "partial",
            True,
        )

        instance = self.get_object()

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        serializer.save()

        return Response(
            OrderSerializer(instance).data,
            status=status.HTTP_200_OK,
        )

        return obj


class OrderCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(
        self,
        request,
        business_user_id,
    ):
        User = get_user_model()

        user = get_object_or_404(
            User,
            id=business_user_id,
        )

        order_count = Order.objects.filter(
            business_user=user,
            status="in_progress",
        ).count()

        serializer = OrderCountSerializer(
            {
                "order_count": order_count,
            }
        )

        return Response(serializer.data)
