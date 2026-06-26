"""
URL configuration for the profile API.
"""

from django.urls import path
from .views import BusinessProfilesView, CustomerProfilesView, ProfileDetailView

urlpatterns = [
    path("profile/<int:pk>/", ProfileDetailView.as_view()),
    path("profiles/business/", BusinessProfilesView.as_view()),
    path("profiles/customer/", CustomerProfilesView.as_view()),
]
