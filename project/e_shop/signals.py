from django.db.models.signals import post_save
from django.dispatch import receiver

from e_shop.models import Order, OrderType
from users.models import User


@receiver(post_save, sender=User)
def chech_user_has_basket(sender, **kwargs):
    user = kwargs["instance"]
    basket = user.order_set.filter(order_type=OrderType.basket).exists()
    if basket is False:
        Order.objects.create(user=user, order_type=OrderType.basket, is_pending=False)
