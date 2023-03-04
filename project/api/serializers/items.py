from rest_framework import serializers

from e_shop.models import Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["id", "name", "price"]


class ItemShortSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Item
        fields = ["id"]
