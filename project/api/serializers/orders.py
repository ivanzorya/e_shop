from rest_framework import serializers

from api.serializers.items import ItemSerializer
from api.serializers.vouchers import UserVoucherShortSerializer
from e_shop.models import Order, OrderItem


class OrderCompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["payment_option"]
        extra_kwargs = {"payment_option": {"required": True}}


class OrderItemAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["item", "quantity"]


class OrderItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer()

    class Meta:
        model = OrderItem
        fields = ["item", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(source="orderitem_set", many=True)
    total_amount = serializers.SerializerMethodField()
    user_voucher = UserVoucherShortSerializer()

    class Meta:
        model = Order
        fields = ["id", "payment_option", "order_type", "is_pending", "items", "total_amount", "user_voucher"]

    def get_total_amount(self, order):
        return order.get_total_amount()
