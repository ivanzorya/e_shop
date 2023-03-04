from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers import ItemSerializer, ItemShortSerializer
from e_shop.models import Item


class FavoritesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = self.request.user.favorite_items.all()
            return queryset
        return []

    @swagger_auto_schema(
        request_body=ItemShortSerializer,
        responses={
            status.HTTP_200_OK: ItemSerializer,
        },
    )
    @action(detail=False, methods=["patch"], url_name="add-item")
    def add_item(self, request):
        serializer = ItemShortSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        item = get_object_or_404(Item, pk=serializer.data["id"])
        request.user.favorite_items.add(item)

        serializer = ItemSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=ItemShortSerializer,
        responses={
            status.HTTP_200_OK: ItemShortSerializer,
        },
    )
    @action(detail=False, methods=["patch"], url_name="remove-item")
    def remove_item(self, request):
        serializer = ItemShortSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = get_object_or_404(Item, pk=serializer.data["id"])
        request.user.favorite_items.remove(item)
        return Response(serializer.data, status=status.HTTP_200_OK)
