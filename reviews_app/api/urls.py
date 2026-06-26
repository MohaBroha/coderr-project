from django.urls import path

from .views import ReviewListView, ReviewDetailView

urlpatterns = [
    path(
        "reviews/",
        ReviewListView.as_view(),
    ),
    path(
        "reviews/<int:pk>/",
        ReviewDetailView.as_view(),
    ),
]
