from django.urls import reverse

from tests.mixins.mixins import EShopTestCase


class VouchersTestCase(EShopTestCase):
    def test_get_vouchers_list(self):
        response = self.client.get(reverse("vouchers-list"))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

        self.api_client.force_authenticate(self.user_2)
        response = self.api_client.get(reverse("vouchers-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 0)

        self.api_client.force_authenticate(self.user_1)
        response = self.api_client.get(reverse("vouchers-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 2)
        self.assertEqual(response.data["results"][0]["voucher"]["item"]["id"], self.item_3.id)
        self.assertEqual(response.data["results"][1]["voucher"]["item"]["id"], self.item_1.id)
