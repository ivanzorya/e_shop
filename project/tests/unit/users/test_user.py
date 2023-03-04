from model_bakery import baker

from e_shop.models import Order, OrderType
from tests.mixins.mixins import EShopTestCase


class UserTestCase(EShopTestCase):
    def test_create_user_signal(self):
        self.assertTrue(self.admin.order_set.filter(order_type=OrderType.basket).exists())

    def test_get_basket(self):
        self.assertIsNotNone(self.user_1.get_basket())
        self.assertIsInstance(self.user_1.get_basket(), Order)
        self.assertIsNotNone(self.user_2.get_basket())
        self.assertIsInstance(self.user_2.get_basket(), Order)
        user_3 = baker.make(
            "users.User",
            email="user3@test.com",
            is_active=True,
        )
        self.assertIsNotNone(user_3.get_basket())
        self.assertIsInstance(user_3.get_basket(), Order)
