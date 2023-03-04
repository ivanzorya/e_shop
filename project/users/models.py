from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from e_shop.models import OrderType
from users.managers import CustomUserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    favorite_items = models.ManyToManyField("e_shop.Item", blank=True)
    vouchers = models.ManyToManyField("e_shop.Voucher", through="e_shop.UserVoucher")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_basket(self):
        return self.order_set.get(order_type=OrderType.basket)
