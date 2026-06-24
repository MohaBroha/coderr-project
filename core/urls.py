from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("auth_app.api.urls")),
    path("api/", include("profile_app.urls")),
    path("api/", include("offers_app.urls")),
    path("api/", include("orders_app.urls")),
    path(
        "api/",
        include("reviews_app.urls"),
    ),
]
