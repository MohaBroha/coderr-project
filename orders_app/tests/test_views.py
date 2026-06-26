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

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

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

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            0,
        )


class OrderCreateViewTests(APITestCase):

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


class OrderPatchViewTests(APITestCase):

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

        self.order = Order.objects.create(
            customer_user=self.customer,
            business_user=self.business,
            title="Logo Design",
            revisions=2,
            delivery_time=5,
            price=150,
            features=["Logo"],
            offer_type="basic",
            status="in_progress",
        )

    def test_patch_requires_authentication(self):
        response = self.client.patch(
            f"/api/orders/{self.order.id}/",
            {"status": "completed"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_customer_cannot_patch_order(self):
        self.client.force_authenticate(
            user=self.customer,
        )

        response = self.client.patch(
            f"/api/orders/{self.order.id}/",
            {"status": "completed"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_business_owner_can_patch_order(self):
        self.client.force_authenticate(
            user=self.business,
        )

        response = self.client.patch(
            f"/api/orders/{self.order.id}/",
            {"status": "completed"},
            format="json",
        )

        self.order.refresh_from_db()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            self.order.status,
            "completed",
        )

    def test_other_business_cannot_patch_order(self):
        other_business = User.objects.create_user(
            username="other_business",
            password="test12345",
        )

        Profile.objects.create(
            user=other_business,
            type="business",
        )

        self.client.force_authenticate(
            user=other_business,
        )

        response = self.client.patch(
            f"/api/orders/{self.order.id}/",
            {"status": "completed"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_patch_non_existing_order_returns_404(self):
        self.client.force_authenticate(
            user=self.business,
        )

        response = self.client.patch(
            "/api/orders/999999/",
            {"status": "completed"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_patch_invalid_status_returns_400(self):
        self.client.force_authenticate(
            user=self.business,
        )

        response = self.client.patch(
            f"/api/orders/{self.order.id}/",
            {"status": "invalid"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_patch_invalid_field_returns_400(self):
        self.client.force_authenticate(
            user=self.business,
        )

        response = self.client.patch(
            f"/api/orders/{self.order.id}/",
            {
                "title": "New Title",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )


class OrderDeleteViewTests(APITestCase):

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

        self.staff = User.objects.create_user(
            username="admin",
            password="test12345",
            is_staff=True,
        )

        self.order = Order.objects.create(
            customer_user=self.customer,
            business_user=self.business,
            title="Logo Design",
            revisions=2,
            delivery_time=5,
            price=150,
            features=["Logo"],
            offer_type="basic",
            status="in_progress",
        )

    def test_delete_requires_authentication(self):
        response = self.client.delete(
            f"/api/orders/{self.order.id}/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_business_cannot_delete_order(self):
        self.client.force_authenticate(
            user=self.business,
        )

        response = self.client.delete(
            f"/api/orders/{self.order.id}/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_customer_cannot_delete_order(self):
        self.client.force_authenticate(
            user=self.customer,
        )

        response = self.client.delete(
            f"/api/orders/{self.order.id}/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_staff_can_delete_order(self):
        self.client.force_authenticate(
            user=self.staff,
        )

        response = self.client.delete(
            f"/api/orders/{self.order.id}/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Order.objects.filter(
                id=self.order.id,
            ).exists()
        )

    def test_delete_non_existing_order_returns_404(self):
        self.client.force_authenticate(
            user=self.staff,
        )

        response = self.client.delete(
            "/api/orders/999999/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )


class OrderCountViewTests(APITestCase):

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

        Order.objects.create(
            customer_user=self.customer,
            business_user=self.business,
            title="Order 1",
            revisions=1,
            delivery_time=3,
            price=100,
            features=[],
            offer_type="basic",
            status="in_progress",
        )

        Order.objects.create(
            customer_user=self.customer,
            business_user=self.business,
            title="Order 2",
            revisions=1,
            delivery_time=3,
            price=100,
            features=[],
            offer_type="basic",
            status="in_progress",
        )

        Order.objects.create(
            customer_user=self.customer,
            business_user=self.business,
            title="Completed",
            revisions=1,
            delivery_time=3,
            price=100,
            features=[],
            offer_type="basic",
            status="completed",
        )

        self.url = f"/api/order-count/{self.business.id}/"

    def test_order_count_requires_authentication(self):
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_order_count_returns_correct_number(self):
        self.client.force_authenticate(
            user=self.customer,
        )

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["order_count"],
            2,
        )

    def test_order_count_returns_404_for_unknown_business(self):
        self.client.force_authenticate(
            user=self.customer,
        )

        response = self.client.get(
            "/api/order-count/999999/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )


class CompletedOrderCountViewTests(APITestCase):

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

        Order.objects.create(
            customer_user=self.customer,
            business_user=self.business,
            title="Completed 1",
            revisions=1,
            delivery_time=3,
            price=100,
            features=[],
            offer_type="basic",
            status="completed",
        )

        Order.objects.create(
            customer_user=self.customer,
            business_user=self.business,
            title="Completed 2",
            revisions=1,
            delivery_time=3,
            price=100,
            features=[],
            offer_type="basic",
            status="completed",
        )

        Order.objects.create(
            customer_user=self.customer,
            business_user=self.business,
            title="In Progress",
            revisions=1,
            delivery_time=3,
            price=100,
            features=[],
            offer_type="basic",
            status="in_progress",
        )

        self.url = f"/api/completed-order-count/{self.business.id}/"

    def test_completed_order_count_requires_authentication(self):
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_completed_order_count_returns_correct_number(self):
        self.client.force_authenticate(
            user=self.customer,
        )

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["completed_order_count"],
            2,
        )

    def test_completed_order_count_returns_404_for_unknown_business(self):
        self.client.force_authenticate(
            user=self.customer,
        )

        response = self.client.get(
            "/api/completed-order-count/999999/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )
