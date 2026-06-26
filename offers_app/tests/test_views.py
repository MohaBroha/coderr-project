from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from offers_app.models import Offer, OfferDetail


class TestOfferListView(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="business",
            password="test12345",
            is_staff=True,
        )

        self.token = Token.objects.create(
            user=self.user,
        )

        self.offer = Offer.objects.create(
            user=self.user,
            title="Website Design",
            description="Professionelles Website-Design",
        )

        OfferDetail.objects.create(
            offer=self.offer,
            title="Basic",
            revisions=1,
            price=100,
            delivery_time=7,
            features=["A"],
            offer_type="basic",
        )

    def test_get_offers_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        response = self.client.get("/api/offers/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["count"],
            1,
        )

        self.assertEqual(
            response.data["results"][0]["title"],
            "Website Design",
        )

        self.assertEqual(
            response.data["results"][0]["min_price"],
            100,
        )

        self.assertEqual(
            response.data["results"][0]["min_delivery_time"],
            7,
        )

        self.assertIn(
            "user_details",
            response.data["results"][0],
        )

        self.assertEqual(
            response.data["results"][0]["details"][0]["url"],
            f"/offerdetails/{self.offer.details.first().id}/",
        )

    def test_get_offers_without_authentication(self):
        response = self.client.get(
            "/api/offers/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["count"],
            1,
        )

    def test_create_offer_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        data = {
            "title": "Grafikdesign-Paket",
            "image": None,
            "description": "Ein umfassendes Grafikdesign-Paket.",
            "details": [
                {
                    "title": "Basic",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": 100,
                    "features": ["Logo"],
                    "offer_type": "basic",
                },
                {
                    "title": "Standard",
                    "revisions": 5,
                    "delivery_time_in_days": 7,
                    "price": 200,
                    "features": ["Logo", "Flyer"],
                    "offer_type": "standard",
                },
                {
                    "title": "Premium",
                    "revisions": 10,
                    "delivery_time_in_days": 10,
                    "price": 500,
                    "features": [
                        "Logo",
                        "Flyer",
                        "Website",
                    ],
                    "offer_type": "premium",
                },
            ],
        }

        response = self.client.post(
            "/api/offers/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            response.data["title"],
            "Grafikdesign-Paket",
        )

        self.assertEqual(
            len(response.data["details"]),
            3,
        )

        self.assertIn(
            "id",
            response.data,
        )

        self.assertIn(
            "id",
            response.data["details"][0],
        )

    def test_create_offer_unauthorized(self):
        data = {
            "title": "Test",
            "description": "Test",
            "details": [],
        }

        response = self.client.post(
            "/api/offers/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_create_offer_invalid_details(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        data = {
            "title": "Test",
            "description": "Test",
            "details": [
                {
                    "title": "Basic",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": 100,
                    "features": ["Logo"],
                    "offer_type": "basic",
                },
                {
                    "title": "Standard",
                    "revisions": 5,
                    "delivery_time_in_days": 7,
                    "price": 200,
                    "features": ["Logo"],
                    "offer_type": "standard",
                },
            ],
        }

        response = self.client.post(
            "/api/offers/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_create_offer_missing_title(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        data = {
            "description": "Test",
            "details": [
                {
                    "title": "Basic",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": 100,
                    "features": ["Logo"],
                    "offer_type": "basic",
                },
                {
                    "title": "Standard",
                    "revisions": 5,
                    "delivery_time_in_days": 7,
                    "price": 200,
                    "features": ["Logo"],
                    "offer_type": "standard",
                },
                {
                    "title": "Premium",
                    "revisions": 10,
                    "delivery_time_in_days": 10,
                    "price": 500,
                    "features": ["Logo"],
                    "offer_type": "premium",
                },
            ],
        }

        response = self.client.post(
            "/api/offers/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_get_offer_detail_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        response = self.client.get(
            f"/api/offers/{self.offer.id}/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["id"],
            self.offer.id,
        )

        self.assertEqual(
            response.data["title"],
            "Website Design",
        )

        self.assertEqual(
            response.data["min_price"],
            100,
        )

        self.assertEqual(
            response.data["min_delivery_time"],
            7,
        )

        self.assertEqual(
            response.data["details"][0]["id"],
            self.offer.details.first().id,
        )

        self.assertEqual(
            response.data["details"][0]["url"],
            f"http://testserver/api/offerdetails/{self.offer.details.first().id}/",
        )

    def test_get_offer_detail_unauthorized(self):
        response = self.client.get(
            f"/api/offers/{self.offer.id}/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_get_offer_detail_not_found(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        response = self.client.get(
            "/api/offers/999999/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_patch_offer_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        data = {
            "title": "Updated Website Design",
            "details": [
                {
                    "title": "Basic Updated",
                    "revisions": 3,
                    "delivery_time_in_days": 6,
                    "price": 120,
                    "features": [
                        "Logo",
                        "Flyer",
                    ],
                    "offer_type": "basic",
                }
            ],
        }

        response = self.client.patch(
            f"/api/offers/{self.offer.id}/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["title"],
            "Updated Website Design",
        )

        self.assertEqual(
            response.data["details"][0]["title"],
            "Basic Updated",
        )

        self.assertEqual(
            response.data["details"][0]["price"],
            120,
        )

        self.assertEqual(
            response.data["details"][0]["delivery_time_in_days"],
            6,
        )

        self.assertEqual(
            response.data["details"][0]["id"],
            self.offer.details.first().id,
        )

    def test_patch_offer_unauthorized(self):
        response = self.client.patch(
            f"/api/offers/{self.offer.id}/",
            {
                "title": "Updated",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_patch_offer_forbidden(self):
        other_user = User.objects.create_user(
            username="other_business",
            password="test12345",
            is_staff=True,
        )

        other_token = Token.objects.create(
            user=other_user,
        )

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {other_token.key}")

        response = self.client.patch(
            f"/api/offers/{self.offer.id}/",
            {
                "title": "Hack",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_patch_offer_not_found(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        response = self.client.patch(
            "/api/offers/999999/",
            {
                "title": "Updated",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_delete_offer_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        response = self.client.delete(
            f"/api/offers/{self.offer.id}/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Offer.objects.filter(
                id=self.offer.id,
            ).exists()
        )

    def test_delete_offer_unauthorized(self):
        response = self.client.delete(
            f"/api/offers/{self.offer.id}/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_delete_offer_forbidden(self):
        other_user = User.objects.create_user(
            username="other_business_delete",
            password="test12345",
            is_staff=True,
        )

        other_token = Token.objects.create(
            user=other_user,
        )

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {other_token.key}")

        response = self.client.delete(
            f"/api/offers/{self.offer.id}/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_delete_offer_not_found(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        response = self.client.delete(
            "/api/offers/999999/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_get_offer_detail_retrieve_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        detail = self.offer.details.first()

        response = self.client.get(
            f"/api/offerdetails/{detail.id}/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["id"],
            detail.id,
        )

        self.assertEqual(
            response.data["title"],
            detail.title,
        )

        self.assertEqual(
            response.data["price"],
            detail.price,
        )

        self.assertEqual(
            response.data["delivery_time_in_days"],
            detail.delivery_time,
        )

        self.assertEqual(
            response.data["offer_type"],
            detail.offer_type,
        )

    def test_get_offer_detail_retrieve_unauthorized(self):
        detail = self.offer.details.first()

        response = self.client.get(
            f"/api/offerdetails/{detail.id}/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_get_offer_detail_retrieve_not_found(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        response = self.client.get(
            "/api/offerdetails/999999/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )
