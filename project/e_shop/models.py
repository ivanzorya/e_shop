from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class PaymentOption(models.TextChoices):
    paypal = "pay_pal", "pay_pal"
    credit_card = "credit_card", "credit_card"


class OrderType(models.TextChoices):
    order = "order", "order"
    basket = "basket", "basket"


class TimestampableIndexedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        abstract = True
        ordering = ["-id"]


class Item(TimestampableIndexedMixin):
    name = models.CharField(max_length=150)
    price = models.PositiveIntegerField()


class Order(TimestampableIndexedMixin):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    payment_option = models.CharField(max_length=11, blank=True, null=True, choices=PaymentOption.choices)
    order_type = models.CharField(max_length=6, choices=OrderType.choices)
    is_pending = models.BooleanField(default=True)
    items = models.ManyToManyField(Item, through="OrderItem")
    user_voucher = models.OneToOneField("UserVoucher", on_delete=models.SET_NULL, blank=True, null=True)

    def get_total_amount(self):
        total_amount = 0
        for order_item in self.orderitem_set.all():
            item_amount = order_item.item.price * order_item.quantity
            if self.user_voucher and self.user_voucher.voucher.item == order_item.item:
                item_amount *= 1 - (self.user_voucher.voucher.discount / 100)
            total_amount += item_amount
        return total_amount

    def complete_order(self, payment_option):
        self.order_type = OrderType.order
        self.payment_option = payment_option
        self.is_pending = True
        self.save()
        Order.objects.create(user=self.user, order_type=OrderType.basket, is_pending=False)


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class Voucher(TimestampableIndexedMixin):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    discount = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])


class UserVoucher(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-id"]
