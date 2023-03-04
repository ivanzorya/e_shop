from e_shop.models import OrderType
from tests.mixins.mixins import EShopTestCase


class CreateUserTestCase(EShopTestCase):
    def test_create_user_signal(self):
        self.assertTrue(self.admin.order_set.filter(order_type=OrderType.basket).exists())
