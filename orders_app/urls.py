from django.urls import path

from .views import OrderListView, OrderDetailView, OrderCountView

urlpatterns = [
    path("orders/", OrderListView.as_view()),
    path("orders/<int:pk>/", OrderDetailView.as_view()),
    path(
        "order-count/<int:business_user_id>/",
        OrderCountView.as_view(),
    ),
]
