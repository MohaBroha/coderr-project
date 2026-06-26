from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from rest_framework.permissions import IsAuthenticated

from ..models import Review
from .serializer import ReviewSerializer, ReviewCreateSerializer, ReviewUpdateSerializer
from rest_framework import status
from rest_framework.response import Response
from .permissions import IsCustomerUser, IsReviewOwner


class ReviewListView(ListCreateAPIView):
    """
    API view for listing and creating reviews.
    """

    queryset = Review.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = None

    filter_backends = [OrderingFilter]

    ordering_fields = [
        "updated_at",
        "rating",
    ]

    def get_queryset(self):
        """
        Return reviews filtered by business user or reviewer if provided.
        """
        queryset = Review.objects.all()

        business_user_id = self.request.query_params.get("business_user_id")
        reviewer_id = self.request.query_params.get("reviewer_id")

        if business_user_id:
            queryset = queryset.filter(business_user_id=business_user_id)

        if reviewer_id:
            queryset = queryset.filter(reviewer_id=reviewer_id)

        return queryset

    def get_serializer_class(self):
        """
        Return the serializer class for the current request.
        """
        if self.request.method == "POST":
            return ReviewCreateSerializer

        return ReviewSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new review and return its serialized representation.
        """
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        review = serializer.save()

        return Response(
            ReviewSerializer(review).data,
            status=status.HTTP_201_CREATED,
        )

    def get_permissions(self):
        """
        Return the permissions required for the current request.
        """
        if self.request.method == "POST":
            return [
                IsAuthenticated(),
                IsCustomerUser(),
            ]

        return [
            IsAuthenticated(),
        ]


class ReviewDetailView(RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting reviews.
    """

    queryset = Review.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """
        Return the serializer class for the current request.
        """
        if self.request.method == "PATCH":
            return ReviewUpdateSerializer

        return ReviewSerializer

    def get_permissions(self):
        """
        Return the permissions required for the current request.
        """
        if self.request.method in ["PATCH", "DELETE"]:
            return [
                IsAuthenticated(),
                IsReviewOwner(),
            ]

        return [
            IsAuthenticated(),
        ]

    def update(self, request, *args, **kwargs):
        """
        Update a review and return its serialized representation.
        """
        partial = kwargs.pop("partial", False)

        instance = self.get_object()

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial,
        )

        serializer.is_valid(raise_exception=True)

        review = serializer.save()

        return Response(ReviewSerializer(review).data)
