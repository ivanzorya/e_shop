import random

from django.core.management.base import BaseCommand

from e_shop.models import Item


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            for _ in range(100):
                name = f"item {random.randint(1, 1000)}"
                price = random.randint(1, 1000)
                Item.objects.create(name=name, price=price)
            return "Success"
        except Exception:
            return "Fail"
