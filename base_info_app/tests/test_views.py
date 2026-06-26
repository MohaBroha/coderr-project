from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from offers_app.models import Offer
from profile_app.models import Profile
from reviews_app.models import Review


class BaseInfoViewTests(APITestCase):

    def setUp(self):
        self.business = User.objects.create_user(
            username="business",
            password="test12345",
        )

        Profile.objects.create(
            user=self.business,
            type="business",
        )

        self.customer = User.objects.create_user(
            username="customer",
            password="test12345",
        )

        Profile.objects.create(
            user=self.customer,
            type="customer",
        )

        Offer.objects.create(
            user=self.business,
            title="Logo Design",
            description="Description",
        )

        Review.objects.create(
            business_user=self.business,
            reviewer=self.customer,
            rating=4,
            description="Very good",
        )

        Review.objects.create(
            business_user=self.business,
            reviewer=User.objects.create_user(
                username="customer2",
                password="test12345",
            ),
            rating=5,
            description="Excellent",
        )

        self.url = "/api/base-info/"

    def test_base_info_returns_200(self):
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_base_info_contains_all_required_fields(self):
        response = self.client.get(self.url)

        self.assertIn(
            "review_count",
            response.data,
        )

        self.assertIn(
            "average_rating",
            response.data,
        )

        self.assertIn(
            "business_profile_count",
            response.data,
        )

        self.assertIn(
            "offer_count",
            response.data,
        )

    def test_average_rating_is_rounded_to_one_decimal(self):
        response = self.client.get(self.url)

        self.assertEqual(
            response.data["review_count"],
            2,
        )

        self.assertEqual(
            response.data["business_profile_count"],
            1,
        )

        self.assertEqual(
            response.data["offer_count"],
            1,
        )

        self.assertEqual(
            response.data["average_rating"],
            4.5,
        )
