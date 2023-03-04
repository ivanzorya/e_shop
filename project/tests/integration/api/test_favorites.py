from django.urls import reverse

from tests.mixins.mixins import EShopTestCase


class FavoritesTestCase(EShopTestCase):
    def test_get_favorites_list(self):
        response = self.client.get(reverse("favorites-list"))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

        self.api_client.force_authenticate(self.user_2)
        response = self.api_client.get(reverse("favorites-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 0)

        self.api_client.force_authenticate(self.user_1)
        response = self.api_client.get(reverse("favorites-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 2)
        self.assertEqual(response.data["results"][0]["id"], self.item_3.id)
        self.assertEqual(response.data["results"][1]["id"], self.item_1.id)

    def test_add_favorite_item(self):
        response = self.client.patch(reverse("favorites-add-item"))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

        self.assertFalse(self.user_2.favorite_items.exists())

        self.api_client.force_authenticate(self.user_2)
        response = self.api_client.patch(reverse("favorites-add-item"), data={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["id"][0], "This field is required.")

        data = {"id": self.item_4.id + 100}
        response = self.api_client.patch(reverse("favorites-add-item"), data=data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["detail"], "Not found.")

        data["id"] = self.item_2.id
        response = self.api_client.patch(reverse("favorites-add-item"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], self.item_2.id)
        self.assertTrue(self.user_2.favorite_items.filter(id=self.item_2.id).exists())

        response = self.api_client.patch(reverse("favorites-add-item"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], self.item_2.id)
        self.assertEqual(self.user_2.favorite_items.filter(id=self.item_2.id).count(), 1)

    def test_remove_favorite_item(self):
        response = self.client.patch(reverse("favorites-remove-item"))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

        self.assertFalse(self.user_2.favorite_items.exists())

        self.api_client.force_authenticate(self.user_2)
        response = self.api_client.patch(reverse("favorites-remove-item"), data={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["id"][0], "This field is required.")

        data = {"id": self.item_4.id + 100}
        response = self.api_client.patch(reverse("favorites-remove-item"), data=data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["detail"], "Not found.")

        data["id"] = self.item_2.id
        response = self.api_client.patch(reverse("favorites-remove-item"), data=data)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(self.user_1.favorite_items.filter(id=self.item_1.id).count(), 1)

        self.api_client.force_authenticate(self.user_1)
        data["id"] = self.item_1.id
        response = self.api_client.patch(reverse("favorites-remove-item"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], self.item_1.id)
        self.assertEqual(self.user_1.favorite_items.filter(id=self.item_1.id).count(), 0)
