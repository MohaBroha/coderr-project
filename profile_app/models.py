from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    USER_TYPE = (
        ("customer", "Customer"),
        ("business", "Business"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=USER_TYPE)

    first_name = models.CharField(max_length=255, blank=True, default="")
    last_name = models.CharField(max_length=255, blank=True, default="")
    location = models.CharField(max_length=255, blank=True, default="")
    tel = models.CharField(max_length=50, blank=True, default="")
    description = models.TextField(blank=True, default="")
    working_hours = models.CharField(max_length=100, blank=True, default="")

    file = models.CharField(max_length=255, blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)
