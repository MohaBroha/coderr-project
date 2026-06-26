from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from profile_app.models import Profile
from reviews_app.models import Review


class ReviewListViewTests(APITestCase):

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

        self.business2 = User.objects.create_user(
            username="business2",
            password="test12345",
        )

        Profile.objects.create(
            user=self.business2,
            type="business",
        )

        self.customer2 = User.objects.create_user(
            username="customer2",
            password="test12345",
        )

        Profile.objects.create(
            user=self.customer2,
            type="customer",
        )

        self.review1 = Review.objects.create(
            business_user=self.business,
            reviewer=self.customer,
            rating=5,
            description="Excellent",
        )

        self.review2 = Review.objects.create(
            business_user=self.business2,
            reviewer=self.customer2,
            rating=3,
            description="Good",
        )

        self.url = "/api/reviews/"

    def test_get_reviews_requires_authentication(self):
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_authenticated_user_receives_reviews(self):
        self.client.force_authenticate(
            user=self.customer,
        )

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            2,
        )

    def test_filter_by_business_user(self):
        self.client.force_authenticate(
            user=self.customer,
        )

        response = self.client.get(f"{self.url}?business_user_id={self.business.id}")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

        self.assertEqual(
            response.data[0]["business_user"],
            self.business.id,
        )

    def test_filter_by_reviewer(self):
        self.client.force_authenticate(
            user=self.customer,
        )

        response = self.client.get(f"{self.url}?reviewer_id={self.customer.id}")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

        self.assertEqual(
            response.data[0]["reviewer"],
            self.customer.id,
        )

    def test_ordering_by_rating(self):
        self.client.force_authenticate(
            user=self.customer,
        )

        response = self.client.get(f"{self.url}?ordering=rating")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data[0]["rating"],
            3,
        )

        self.assertEqual(
            response.data[1]["rating"],
            5,
        )

    def test_ordering_by_updated_at(self):
        self.client.force_authenticate(
            user=self.customer,
        )

        response = self.client.get(f"{self.url}?ordering=updated_at")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            2,
        )


class ReviewCreateViewTests(APITestCase):

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

        self.business2 = User.objects.create_user(
            username="business2",
            password="test12345",
        )

        Profile.objects.create(
            user=self.business2,
            type="business",
        )

        self.url = "/api/reviews/"

    def test_create_review_requires_authentication(self):
        response = self.client.post(
            self.url,
            {
                "business_user": self.business.id,
                "rating": 5,
                "description": "Excellent",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_customer_can_create_review(self):
        self.client.force_authenticate(
            user=self.customer,
        )

        response = self.client.post(
            self.url,
            {
                "business_user": self.business.id,
                "rating": 5,
                "description": "Excellent",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            Review.objects.count(),
            1,
        )

        self.assertEqual(
            response.data["reviewer"],
            self.customer.id,
        )

    def test_business_cannot_create_review(self):
        self.client.force_authenticate(
            user=self.business,
        )

        response = self.client.post(
            self.url,
            {
                "business_user": self.business2.id,
                "rating": 5,
                "description": "Excellent",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_create_review_without_required_fields_returns_400(self):
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

    def test_duplicate_review_returns_403(self):
        Review.objects.create(
            business_user=self.business,
            reviewer=self.customer,
            rating=5,
            description="Excellent",
        )

        self.client.force_authenticate(
            user=self.customer,
        )

        response = self.client.post(
            self.url,
            {
                "business_user": self.business.id,
                "rating": 4,
                "description": "Again",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_customer_cannot_review_himself(self):
        self.client.force_authenticate(
            user=self.customer,
        )

        response = self.client.post(
            self.url,
            {
                "business_user": self.customer.id,
                "rating": 5,
                "description": "Self review",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )


class ReviewPatchViewTests(APITestCase):

    def setUp(self):
        self.customer = User.objects.create_user(
            username="customer",
            password="test12345",
        )

        Profile.objects.create(
            user=self.customer,
            type="customer",
        )

        self.other_customer = User.objects.create_user(
            username="other_customer",
            password="test12345",
        )

        Profile.objects.create(
            user=self.other_customer,
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

        self.review = Review.objects.create(
            business_user=self.business,
            reviewer=self.customer,
            rating=4,
            description="Very good",
        )

    def test_patch_requires_authentication(self):
        response = self.client.patch(
            f"/api/reviews/{self.review.id}/",
            {
                "rating": 5,
                "description": "Excellent",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_review_owner_can_patch_review(self):
        self.client.force_authenticate(
            user=self.customer,
        )

        response = self.client.patch(
            f"/api/reviews/{self.review.id}/",
            {
                "rating": 5,
                "description": "Excellent",
            },
            format="json",
        )

        self.review.refresh_from_db()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            self.review.rating,
            5,
        )

        self.assertEqual(
            self.review.description,
            "Excellent",
        )

    def test_other_customer_cannot_patch_review(self):
        self.client.force_authenticate(
            user=self.other_customer,
        )

        response = self.client.patch(
            f"/api/reviews/{self.review.id}/",
            {
                "rating": 5,
                "description": "Excellent",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_patch_non_existing_review_returns_404(self):
        self.client.force_authenticate(
            user=self.customer,
        )

        response = self.client.patch(
            "/api/reviews/999999/",
            {
                "rating": 5,
                "description": "Excellent",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_patch_invalid_rating_returns_400(self):
        self.client.force_authenticate(
            user=self.customer,
        )

        response = self.client.patch(
            f"/api/reviews/{self.review.id}/",
            {
                "rating": 6,
                "description": "Excellent",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )


class ReviewDeleteViewTests(APITestCase):

    def setUp(self):
        self.customer = User.objects.create_user(
            username="customer",
            password="test12345",
        )

        Profile.objects.create(
            user=self.customer,
            type="customer",
        )

        self.other_customer = User.objects.create_user(
            username="other_customer",
            password="test12345",
        )

        Profile.objects.create(
            user=self.other_customer,
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

        self.review = Review.objects.create(
            business_user=self.business,
            reviewer=self.customer,
            rating=5,
            description="Excellent",
        )

    def test_delete_requires_authentication(self):
        response = self.client.delete(
            f"/api/reviews/{self.review.id}/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_review_owner_can_delete_review(self):
        self.client.force_authenticate(
            user=self.customer,
        )

        response = self.client.delete(
            f"/api/reviews/{self.review.id}/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Review.objects.filter(
                id=self.review.id,
            ).exists()
        )

    def test_other_customer_cannot_delete_review(self):
        self.client.force_authenticate(
            user=self.other_customer,
        )

        response = self.client.delete(
            f"/api/reviews/{self.review.id}/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_delete_non_existing_review_returns_404(self):
        self.client.force_authenticate(
            user=self.customer,
        )

        response = self.client.delete(
            "/api/reviews/999999/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )
