from rest_framework import serializers

from api.serializers.items import ItemSerializer
from e_shop.models import UserVoucher, Voucher


class VoucherSerializer(serializers.ModelSerializer):
    item = ItemSerializer()

    class Meta:
        model = Voucher
        fields = ["id", "item", "discount"]


class UserVoucherSerializer(serializers.ModelSerializer):
    voucher = VoucherSerializer()

    class Meta:
        model = UserVoucher
        fields = ["id", "voucher", "is_active"]


class UserVoucherIdSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = UserVoucher
        fields = ["id"]


class VoucherShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voucher
        fields = ["item", "discount"]


class UserVoucherShortSerializer(serializers.ModelSerializer):
    voucher = VoucherShortSerializer()

    class Meta:
        model = UserVoucher
        fields = ["id", "voucher"]
