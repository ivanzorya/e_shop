from django.urls import reverse

from tests.mixins.mixins import EShopTestCase
from users.models import User


class UsersTestCase(EShopTestCase):
    def test_create_user(self):
        data = {"email": "user@example.com", "password": "string", "first_name": "string", "last_name": "string"}
        user_exists = User.objects.filter(email=data["email"]).exists()
        self.assertFalse(user_exists)
        response = self.api_client.post(reverse("users-list"), data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["email"], data["email"])

        user_exists = User.objects.filter(email=data["email"]).exists()
        self.assertTrue(user_exists)

        response = self.api_client.post(reverse("users-list"), data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["email"][0], "user with this email address already exists.")

        data["email"] = "fake_email"
        response = self.api_client.post(reverse("users-list"), data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["email"][0], "Enter a valid email address.")

        response = self.api_client.post(reverse("users-list"), data={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["email"][0], "This field is required.")
        self.assertEqual(response.data["password"][0], "This field is required.")

    def test_get_profile(self):
        response = self.client.get(reverse("users-get-profile"))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

        self.api_client.force_authenticate(self.user_2)
        response = self.api_client.get(reverse("users-get-profile"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["email"], self.user_2.email)

        self.api_client.force_authenticate(self.user_1)
        response = self.api_client.get(reverse("users-get-profile"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["email"], self.user_1.email)
