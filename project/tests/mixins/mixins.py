import logging
import uuid

from django.conf import settings
from django.test import TestCase
from model_bakery import baker
from rest_framework.test import APIClient

from e_shop.models import OrderType, PaymentOption

logger = logging.getLogger(settings.DEBUG_LOGGER)


class EShopTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.api_client = APIClient()
        self.setup_users()
        self.setup_items()
        self.setup_vouchers()
        self.setup_favorites()
        self.setup_orders()
        self.setup_baskets()

    def setup_users(self):
        self.admin = baker.make(
            "users.User",
            email="admin@admin.com",
            is_staff=True,
            is_active=True,
        )
        self.user_1 = baker.make(
            "users.User",
            email="user1@test.com",
            is_active=True,
        )
        self.user_1.set_password("test")
        self.user_1.save()
        self.user_2 = baker.make(
            "users.User",
            email="user2@test.com",
            is_active=True,
        )
        self.user_2.set_password("test")
        self.user_2.save()

    def setup_items(self):
        self.item_1 = baker.make(
            "e_shop.Item",
            name=str(uuid.uuid4()),
            price=100,
        )
        self.item_2 = baker.make(
            "e_shop.Item",
            name=str(uuid.uuid4()),
            price=50,
        )
        self.item_3 = baker.make(
            "e_shop.Item",
            name=str(uuid.uuid4()),
            price=20,
        )
        self.item_4 = baker.make(
            "e_shop.Item",
            name=str(uuid.uuid4()),
            price=1000,
        )

    def setup_vouchers(self):
        self.voucher_1 = baker.make(
            "e_shop.Voucher",
            item=self.item_1,
            discount=10,
        )
        self.voucher_2 = baker.make(
            "e_shop.Voucher",
            item=self.item_3,
            discount=20,
        )
        self.user_1_voucher_1 = baker.make("e_shop.UserVoucher", user=self.user_1, voucher=self.voucher_1)
        self.user_1_voucher_2 = baker.make("e_shop.UserVoucher", user=self.user_1, voucher=self.voucher_2)

    def setup_favorites(self):
        self.user_1.favorite_items.add(self.item_1)
        self.user_1.favorite_items.add(self.item_3)

    def setup_orders(self):
        self.order_1 = baker.make(
            "e_shop.Order",
            user=self.user_1,
            payment_option=PaymentOption.credit_card,
            order_type=OrderType.order,
            is_pending=True,
        )
        self.order_1_item_1 = baker.make(
            "e_shop.OrderItem",
            item=self.item_1,
            order=self.order_1,
            quantity=10,
        )
        self.order_1_item_2 = baker.make(
            "e_shop.OrderItem",
            item=self.item_2,
            order=self.order_1,
            quantity=1,
        )
        self.order_2 = baker.make(
            "e_shop.Order",
            user=self.user_1,
            payment_option=PaymentOption.paypal,
            order_type=OrderType.order,
            is_pending=True,
        )
        self.order_2_item_3 = baker.make(
            "e_shop.OrderItem",
            item=self.item_3,
            order=self.order_2,
            quantity=10,
        )
        self.order_2_item_4 = baker.make(
            "e_shop.OrderItem",
            item=self.item_4,
            order=self.order_2,
            quantity=1,
        )

    def setup_baskets(self):
        self.user_2_basket = self.user_2.get_basket()
        baker.make(
            "e_shop.OrderItem",
            item=self.item_1,
            order=self.user_2_basket,
            quantity=10,
        )
        baker.make(
            "e_shop.OrderItem",
            item=self.item_2,
            order=self.user_2_basket,
            quantity=1,
        )
