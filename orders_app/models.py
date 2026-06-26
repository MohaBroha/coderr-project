from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Order(models.Model):
    """
    Model representing an order placed by a customer.
    """

    customer_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="customer_orders",
    )

    business_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="business_orders",
    )

    title = models.CharField(max_length=255)

    revisions = models.IntegerField()

    delivery_time = models.IntegerField()

    price = models.FloatField()

    features = models.JSONField()

    offer_type = models.CharField(max_length=50)

    status = models.CharField(
        max_length=50,
        default="in_progress",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        """
        Return the title of the order.
        """
        return self.title
