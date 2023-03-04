import jwt
from django.conf import settings
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from tests.mixins.mixins import EShopTestCase


class TokenTestCase(EShopTestCase):
    def test_get_token(self):
        response = self.api_client.post(reverse("token_obtain_pair"), data={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["email"][0], "This field is required.")
        self.assertEqual(response.data["password"][0], "This field is required.")

        data = {"email": "fake_email", "password": "fakepass"}
        response = self.api_client.post(reverse("token_obtain_pair"), data=data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["detail"], "No active account found with the given credentials")

        data["email"] = self.user_1.email
        response = self.api_client.post(reverse("token_obtain_pair"), data=data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["detail"], "No active account found with the given credentials")

        data["password"] = "test"
        response = self.api_client.post(reverse("token_obtain_pair"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data.get("access"))
        self.assertIsNotNone(response.data.get("refresh"))
        token_decoded = jwt.decode(response.data["access"], settings.SECRET_KEY, algorithms="HS256")
        self.assertEqual(self.user_1.id, token_decoded["user_id"])

        data["email"] = self.user_2.email
        response = self.api_client.post(reverse("token_obtain_pair"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data.get("access"))
        self.assertIsNotNone(response.data.get("refresh"))
        token_decoded = jwt.decode(response.data["access"], settings.SECRET_KEY, algorithms="HS256")
        self.assertEqual(self.user_2.id, token_decoded["user_id"])

    def test_refresh_token(self):
        response = self.api_client.post(reverse("token_refresh"), data={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["refresh"][0], "This field is required.")

        data = {"refresh": "fake_token"}
        response = self.api_client.post(reverse("token_refresh"), data=data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["detail"], "Token is invalid or expired")

        refresh_token = RefreshToken.for_user(self.user_1)
        data["refresh"] = str(refresh_token)
        response = self.api_client.post(reverse("token_refresh"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data.get("access"))
        token_decoded = jwt.decode(response.data["access"], settings.SECRET_KEY, algorithms="HS256")
        self.assertEqual(self.user_1.id, token_decoded["user_id"])

        refresh_token = RefreshToken.for_user(self.user_2)
        data["refresh"] = str(refresh_token)
        response = self.api_client.post(reverse("token_refresh"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data.get("access"))
        token_decoded = jwt.decode(response.data["access"], settings.SECRET_KEY, algorithms="HS256")
        self.assertEqual(self.user_2.id, token_decoded["user_id"])
