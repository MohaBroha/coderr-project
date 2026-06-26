from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

from profile_app.models import Profile
from orders_app.models import Order
from offers_app.models import Offer, OfferDetail


class OrderListViewTests(APITestCase):

    def setUp(self):
        self.customer = User.objects.create_user(
            username="customer",
            password="test12345",
        )

        Profile.objects.create(
            user=self.customer,
            type="customer",
        )

        self.business = User.objects.create_user(
            username="business",
            password="test12345",
        )

        Profile.objects.create(
            user=self.business,
            type="business",
        )

        self.url = "/api/orders/"

    def test_get_orders_requires_authentication(self):
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_customer_receives_own_orders(self):
        Order.objects.create(
            customer_user=self.customer,
            business_user=self.business,
            title="Design",
            revisions=1,
            delivery_time=3,
            price=100,
            features=[],
            offer_type="basic",
            status="in_progress",
        )

        self.client.force_authenticate(
            user=self.customer,
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_other_users_orders_are_not_returned(self):
        other_customer = User.objects.create_user(
            username="other",
            password="test12345",
        )

        Profile.objects.create(
            user=other_customer,
            type="customer",
        )

        Order.objects.create(
            customer_user=other_customer,
            business_user=self.business,
            title="Hidden",
            revisions=1,
            delivery_time=2,
            price=50,
            features=[],
            offer_type="basic",
            status="in_progress",
        )

        self.client.force_authenticate(
            user=self.customer,
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    from offers_app.models import Offer, OfferDetail

    def setUp(self):
        self.customer = User.objects.create_user(
            username="customer",
            password="test12345",
        )
        Profile.objects.create(
            user=self.customer,
            type="customer",
        )

        self.business = User.objects.create_user(
            username="business",
            password="test12345",
        )
        Profile.objects.create(
            user=self.business,
            type="business",
        )

        self.offer = Offer.objects.create(
            user=self.business,
            title="Logo Design",
            description="Description",
        )

        self.offer_detail = OfferDetail.objects.create(
            offer=self.offer,
            title="Basic",
            revisions=2,
            delivery_time=5,
            price=150,
            features=["Logo", "Visitenkarte"],
            offer_type="basic",
        )

        self.url = "/api/orders/"

    def test_create_order_requires_authentication(self):
        response = self.client.post(
            self.url,
            {"offer_detail_id": self.offer_detail.id},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_customer_can_create_order(self):
        self.client.force_authenticate(
            user=self.customer,
        )

        response = self.client.post(
            self.url,
            {"offer_detail_id": self.offer_detail.id},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            Order.objects.count(),
            1,
        )

    def test_business_cannot_create_order(self):
        self.client.force_authenticate(
            user=self.business,
        )

        response = self.client.post(
            self.url,
            {"offer_detail_id": self.offer_detail.id},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_business_cannot_create_order(self):
        self.client.force_authenticate(
            user=self.business,
        )

        response = self.client.post(
            self.url,
            {"offer_detail_id": self.offer_detail.id},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_create_order_with_invalid_offer_detail_returns_404(self):
        self.client.force_authenticate(
            user=self.customer,
        )

        response = self.client.post(
            self.url,
            {"offer_detail_id": 999999},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_create_order_without_offer_detail_returns_400(self):
        self.client.force_authenticate(
            user=self.customer,
        )

        response = self.client.post(
            self.url,
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
