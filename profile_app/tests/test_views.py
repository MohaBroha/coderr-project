from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from profile_app.models import Profile


class TestProfileDetailView(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="simon",
            password="test12345",
            email="simon@test.de",
        )

        self.profile = Profile.objects.create(
            user=self.user,
            type="customer",
        )

        self.token = Token.objects.create(user=self.user)

    def test_get_profile_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        response = self.client.get(f"/api/profile/{self.user.id}/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["username"],
            "simon",
        )

        self.assertEqual(
            response.data["email"],
            "simon@test.de",
        )

        self.assertEqual(
            response.data["type"],
            "customer",
        )

    def test_get_profile_unauthorized(self):
        response = self.client.get(f"/api/profile/{self.user.id}/")

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_get_profile_not_found(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        response = self.client.get("/api/profile/9999/")

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_get_profile_forbidden(self):
        other_user = User.objects.create_user(
            username="otheruser",
            password="test12345",
        )

        Token.objects.create(user=other_user)

        self.client.force_authenticate(
            user=other_user,
        )

        response = self.client.get(f"/api/profile/{self.user.id}/")

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_patch_profile_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        data = {
            "first_name": "Max",
            "last_name": "Mustermann",
            "location": "Berlin",
            "tel": "987654321",
            "description": "Updated business description",
            "working_hours": "10-18",
        }

        response = self.client.patch(
            f"/api/profile/{self.user.id}/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.profile.refresh_from_db()

        self.assertEqual(
            self.profile.first_name,
            "Max",
        )

        self.assertEqual(
            self.profile.last_name,
            "Mustermann",
        )

        self.assertEqual(
            self.profile.location,
            "Berlin",
        )

    def test_patch_profile_unauthorized(self):
        response = self.client.patch(
            f"/api/profile/{self.user.id}/",
            {
                "first_name": "Max",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_patch_profile_forbidden(self):
        other_user = User.objects.create_user(
            username="otheruser",
            password="test12345",
        )

        other_token = Token.objects.create(
            user=other_user,
        )

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {other_token.key}")

        response = self.client.patch(
            f"/api/profile/{self.user.id}/",
            {
                "first_name": "Hacker",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_patch_profile_not_found(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        response = self.client.patch(
            "/api/profile/9999/",
            {
                "first_name": "Max",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_get_business_profiles_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        business_user = User.objects.create_user(
            username="business",
            password="test12345",
        )

        Profile.objects.create(
            user=business_user,
            type="business",
        )

        response = self.client.get("/api/profiles/business/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(
            len(response.data) > 0,
        )

        self.assertEqual(
            response.data[0]["type"],
            "business",
        )

    def test_get_business_profiles_unauthorized(self):
        response = self.client.get("/api/profiles/business/")

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_get_customer_profiles_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        customer_user = User.objects.create_user(
            username="customer",
            password="test12345",
        )

        Profile.objects.create(
            user=customer_user,
            type="customer",
        )

        response = self.client.get("/api/profiles/customer/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(
            len(response.data) > 0,
        )

        self.assertTrue(all(profile["type"] == "customer" for profile in response.data))

    def test_get_customer_profiles_unauthorized(self):
        response = self.client.get("/api/profiles/customer/")

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
