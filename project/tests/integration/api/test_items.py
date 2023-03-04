from django.urls import reverse

from tests.mixins.mixins import EShopTestCase


class ItemsTestCase(EShopTestCase):
    def test_get_items_list(self):
        response = self.api_client.get(reverse("items-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 4)
        self.assertEqual(response.data["results"][0]["id"], self.item_4.id)
        self.assertEqual(response.data["results"][3]["id"], self.item_1.id)

    def test_get_item(self):
        kwargs = {"pk": self.item_4.id}
        response = self.api_client.get(reverse("items-detail", kwargs=kwargs))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], self.item_4.name)

        kwargs["pk"] = self.item_2.id
        response = self.api_client.get(reverse("items-detail", kwargs=kwargs))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], self.item_2.name)

        kwargs["pk"] = self.item_4.id + 100
        response = self.api_client.get(reverse("items-detail", kwargs=kwargs))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["detail"], "Not found.")
