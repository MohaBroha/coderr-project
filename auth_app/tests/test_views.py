from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase


class TestRegisterView(APITestCase):

    def test_register_user_success(self):
        data = {
            "username": "simon",
            "email": "simon@test.de",
            "password": "test12345",
        }

        response = self.client.post(
            "/api/registration/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        User = get_user_model()

        self.assertTrue(User.objects.filter(username="simon").exists())

        self.assertIn("token", response.data)

        self.assertEqual(
            response.data["username"],
            "simon",
        )

        self.assertEqual(
            response.data["email"],
            "simon@test.de",
        )

        self.assertIn(
            "user_id",
            response.data,
        )

    def test_register_user_without_password(self):
        data = {
            "username": "simon",
            "email": "simon@test.de",
        }

        response = self.client.post(
            "/api/registration/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertIn(
            "password",
            response.data,
        )

    def test_register_duplicate_username(self):
        data = {
            "username": "simon",
            "email": "simon@test.de",
            "password": "test12345",
        }

        self.client.post(
            "/api/registration/",
            data,
            format="json",
        )

        response = self.client.post(
            "/api/registration/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertIn(
            "username",
            response.data,
        )


class TestLoginView(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="simon",
            email="simon@test.de",
            password="test12345",
        )

    def test_login_success(self):
        data = {
            "username": "simon",
            "password": "test12345",
        }

        response = self.client.post(
            "/api/login/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIn(
            "token",
            response.data,
        )

        self.assertEqual(
            response.data["username"],
            "simon",
        )

        self.assertEqual(
            response.data["email"],
            "simon@test.de",
        )

        self.assertIn(
            "user_id",
            response.data,
        )

    def test_login_wrong_password(self):
        data = {
            "username": "simon",
            "password": "wrongpassword",
        }

        response = self.client.post(
            "/api/login/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_login_without_password(self):
        data = {
            "username": "simon",
        }

        response = self.client.post(
            "/api/login/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertIn(
            "password",
            response.data,
        )
