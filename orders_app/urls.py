from django.urls import path

from .views import OrderListView, OrderPatchView

urlpatterns = [
    path("orders/", OrderListView.as_view()),
    path("orders/<int:pk>/", OrderPatchView.as_view()),
]
