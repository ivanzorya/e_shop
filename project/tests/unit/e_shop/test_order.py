from django.core.exceptions import ValidationError
from model_bakery import baker

from e_shop.models import PaymentOption
from tests.mixins.mixins import EShopTestCase


class OrderTestCase(EShopTestCase):
    def test_get_total_amount(self):
        self.assertEqual(self.order_1.get_total_amount(), 1050)
        self.assertEqual(self.order_2.get_total_amount(), 1200)
        self.assertEqual(self.user_2_basket.get_total_amount(), 1050)
        self.assertEqual(self.user_1.get_basket().get_total_amount(), 0)

        user_2_voucher_1 = baker.make("e_shop.UserVoucher", user=self.user_2, voucher=self.voucher_1)
        self.user_2_basket.user_voucher = user_2_voucher_1
        self.user_2_basket.save()
        self.assertEqual(self.user_2_basket.get_total_amount(), 950)

    def test_complete_order(self):
        with self.assertRaises(ValidationError):
            self.order_1.complete_order(PaymentOption.credit_card)
        with self.assertRaises(ValidationError):
            self.order_2.complete_order(PaymentOption.credit_card)
        with self.assertRaises(ValidationError):
            self.user_1.get_basket().complete_order(PaymentOption.credit_card)

        self.user_2_basket.complete_order(PaymentOption.credit_card)
        self.user_2_basket.refresh_from_db()

        self.assertTrue(self.user_2_basket.is_pending)
        self.assertEqual(self.user_2_basket.payment_option, PaymentOption.credit_card)
        self.assertNotEqual(self.user_2_basket.id, self.user_2.get_basket().id)
