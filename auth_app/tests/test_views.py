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
