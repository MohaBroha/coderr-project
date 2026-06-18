from django.urls import path
from .views import OfferDetailView, OfferListView

urlpatterns = [
    path("offers/", OfferListView.as_view()),
    path("offers/<int:pk>/", OfferDetailView.as_view()),
]
