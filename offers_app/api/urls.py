"""
URL configuration for the offers API.
"""

from django.urls import path
from .views import OfferDetailView, OfferListView, OfferDetailRetrieveView

urlpatterns = [
    path("offers/", OfferListView.as_view()),
    path("offers/<int:pk>/", OfferDetailView.as_view()),
    path("offerdetails/<int:pk>/", OfferDetailRetrieveView.as_view()),
]
