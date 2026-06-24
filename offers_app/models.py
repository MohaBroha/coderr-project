from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Offer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class OfferDetail(models.Model):
    offer = models.ForeignKey(Offer, related_name="details", on_delete=models.CASCADE)

    price = models.FloatField()
    delivery_time = models.IntegerField()

    title = models.CharField(max_length=255)
    revisions = models.IntegerField()
    features = models.JSONField()
    offer_type = models.CharField(max_length=50)
