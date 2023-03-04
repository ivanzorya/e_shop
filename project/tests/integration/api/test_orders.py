from django.urls import reverse

from e_shop.models import PaymentOption
from tests.mixins.mixins import EShopTestCase


class OrdersTestCase(EShopTestCase):
    def test_get_orders_list(self):
        response = self.client.get(reverse("orders-list"))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

        self.api_client.force_authenticate(self.user_2)
        response = self.api_client.get(reverse("orders-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 0)

        self.api_client.force_authenticate(self.user_1)
        response = self.api_client.get(reverse("orders-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 2)
        self.assertEqual(response.data["results"][0]["id"], self.order_2.id)
        self.assertEqual(response.data["results"][1]["id"], self.order_1.id)

    def test_get_order(self):
        kwargs = {"pk": self.order_1.id}
        response = self.client.get(reverse("orders-detail", kwargs=kwargs))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

        self.api_client.force_authenticate(self.user_2)
        response = self.api_client.get(reverse("orders-detail", kwargs=kwargs))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["detail"], "Not found.")

        self.api_client.force_authenticate(self.user_1)
        response = self.api_client.get(reverse("orders-detail", kwargs=kwargs))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["items"]), 2)
        self.assertEqual(response.data["items"][1]["item"]["id"], self.item_2.id)
        self.assertEqual(response.data["items"][0]["item"]["id"], self.item_1.id)

    def test_get_basket(self):
        response = self.client.get(reverse("orders-get-basket"))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

        self.api_client.force_authenticate(self.user_2)
        response = self.api_client.get(reverse("orders-get-basket"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["items"]), 2)
        self.assertEqual(response.data["total_amount"], self.user_2_basket.get_total_amount())

        self.api_client.force_authenticate(self.user_1)
        response = self.api_client.get(reverse("orders-get-basket"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["items"]), 0)
        self.assertEqual(response.data["total_amount"], 0)

    def test_add_order_item(self):
        response = self.client.post(reverse("orders-add-item"))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

        self.api_client.force_authenticate(self.user_2)
        response = self.api_client.post(reverse("orders-add-item"), data={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["item"][0], "This field is required.")

        data = {"item": self.item_4.id + 100}
        response = self.api_client.post(reverse("orders-add-item"), data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["item"][0], f"""Invalid pk "{self.item_4.id + 100}" - object does not exist.""")

        self.assertEqual(self.user_2.get_basket().get_total_amount(), 1050)
        data["item"] = self.item_2.id
        response = self.api_client.post(reverse("orders-add-item"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["item"]["name"], self.item_2.name)
        self.assertEqual(response.data["quantity"], 2)
        self.assertEqual(self.user_2.get_basket().get_total_amount(), 1100)

        response = self.api_client.post(reverse("orders-add-item"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["item"]["name"], self.item_2.name)
        self.assertEqual(response.data["quantity"], 3)
        self.assertEqual(self.user_2.get_basket().get_total_amount(), 1150)

        data["quantity"] = 10
        response = self.api_client.post(reverse("orders-add-item"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["item"]["name"], self.item_2.name)
        self.assertEqual(response.data["quantity"], 13)
        self.assertEqual(self.user_2.get_basket().get_total_amount(), 1650)

        self.api_client.force_authenticate(self.user_1)
        self.assertEqual(self.user_1.get_basket().get_total_amount(), 0)
        data = {"item": self.item_2.id}
        response = self.api_client.post(reverse("orders-add-item"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["item"]["name"], self.item_2.name)
        self.assertEqual(response.data["quantity"], 1)
        self.assertEqual(self.user_1.get_basket().get_total_amount(), 50)

        response = self.api_client.post(reverse("orders-add-item"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["item"]["name"], self.item_2.name)
        self.assertEqual(response.data["quantity"], 2)
        self.assertEqual(self.user_1.get_basket().get_total_amount(), 100)

        data["quantity"] = 10
        response = self.api_client.post(reverse("orders-add-item"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["item"]["name"], self.item_2.name)
        self.assertEqual(response.data["quantity"], 12)
        self.assertEqual(self.user_1.get_basket().get_total_amount(), 600)

    def test_remove_order_item(self):
        response = self.client.post(reverse("orders-remove-item"))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

        self.api_client.force_authenticate(self.user_2)
        response = self.api_client.post(reverse("orders-remove-item"), data={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["item"][0], "This field is required.")

        data = {"item": self.item_4.id + 100}
        response = self.api_client.post(reverse("orders-remove-item"), data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["item"][0], f"""Invalid pk "{self.item_4.id + 100}" - object does not exist.""")

        self.assertEqual(self.user_2.get_basket().get_total_amount(), 1050)
        data["item"] = self.item_2.id
        response = self.api_client.post(reverse("orders-remove-item"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user_2.get_basket().get_total_amount(), 1000)

        data["item"] = self.item_1.id
        response = self.api_client.post(reverse("orders-remove-item"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user_2.get_basket().get_total_amount(), 900)

        data["quantity"] = 4
        response = self.api_client.post(reverse("orders-remove-item"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user_2.get_basket().get_total_amount(), 500)

    def test_add_order_voucher(self):
        response = self.client.patch(reverse("orders-add-voucher"))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

        self.assertIsNone(self.user_1.get_basket().user_voucher)

        self.api_client.force_authenticate(self.user_1)
        response = self.api_client.patch(reverse("orders-add-voucher"), data={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["id"][0], "This field is required.")

        data = {"id": self.user_1_voucher_1.id + 100}
        response = self.api_client.patch(reverse("orders-add-voucher"), data=data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["detail"], "Not found.")

        data["id"] = self.user_1_voucher_1.id
        response = self.api_client.patch(reverse("orders-add-voucher"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user_1.get_basket().user_voucher, self.user_1_voucher_1)

        response = self.api_client.patch(reverse("orders-add-voucher"), data=data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["detail"], "Not found.")
        self.assertEqual(self.user_1.get_basket().user_voucher, self.user_1_voucher_1)

    def test_remove_order_voucher(self):
        response = self.client.patch(reverse("orders-remove-voucher"))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

        basket = self.user_1.get_basket()
        basket.user_voucher = self.user_1_voucher_1
        basket.save()
        self.assertEqual(self.user_1.get_basket().user_voucher, self.user_1_voucher_1)

        self.api_client.force_authenticate(self.user_1)
        response = self.api_client.patch(reverse("orders-remove-voucher"))
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(self.user_1.get_basket().user_voucher)

        self.api_client.force_authenticate(self.user_1)
        response = self.api_client.patch(reverse("orders-remove-voucher"))
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(self.user_1.get_basket().user_voucher)

    def test_complete_order(self):
        response = self.client.post(reverse("orders-complete"))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

        self.api_client.force_authenticate(self.user_2)
        response = self.api_client.post(reverse("orders-complete"), data={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["payment_option"][0], "This field is required.")

        data = {"payment_option": "fake_options"}
        response = self.api_client.post(reverse("orders-complete"), data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["payment_option"][0], """"fake_options" is not a valid choice.""")

        data = {"payment_option": PaymentOption.credit_card}
        response = self.api_client.post(reverse("orders-complete"), data=data)
        self.assertEqual(response.status_code, 200)
        self.user_2_basket.refresh_from_db()
        self.assertTrue(self.user_2_basket.is_pending)
        self.assertEqual(self.user_2_basket.payment_option, PaymentOption.credit_card)
        self.assertNotEqual(self.user_2_basket.id, self.user_2.get_basket().id)

        data = {"payment_option": PaymentOption.credit_card}
        response = self.api_client.post(reverse("orders-complete"), data=data)
        self.assertEqual(response.status_code, 400)
