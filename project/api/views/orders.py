import logging

from django.conf import settings
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers import (
    OrderCompleteSerializer,
    OrderItemAddSerializer,
    OrderItemSerializer,
    OrderSerializer,
    UserVoucherIdSerializer,
    UserVoucherShortSerializer,
)
from e_shop.models import Item, Order, OrderItem, OrderType, UserVoucher

logger = logging.getLogger(settings.DEBUG_LOGGER)


class OrderViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        queryset = self.queryset.filter(user__id=self.request.user.id).exclude(order_type=OrderType.basket)
        return queryset

    @action(detail=False, methods=["get"], url_name="get-basket")
    def get_basket(self, request):
        basket = request.user.get_basket()
        serializer = self.serializer_class(basket)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=OrderItemAddSerializer,
        responses={
            status.HTTP_200_OK: OrderItemSerializer,
        },
    )
    @action(detail=False, methods=["post"], url_name="add-item")
    def add_item(self, request):
        serializer = OrderItemAddSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        basket = request.user.get_basket()
        item = get_object_or_404(Item, pk=serializer.data["item"])
        try:
            order_item = OrderItem.objects.get(order=basket, item=item)
            order_item.quantity += serializer.data.get("quantity", 1)
            order_item.save()
        except OrderItem.DoesNotExist:
            order_item = OrderItem.objects.create(order=basket, item=item, quantity=serializer.data.get("quantity", 1))
        serializer = OrderItemSerializer(order_item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=OrderItemAddSerializer,
        responses={
            status.HTTP_200_OK: OrderItemSerializer,
        },
    )
    @action(detail=False, methods=["post"], url_name="remove-item")
    def remove_item(self, request):
        serializer = OrderItemAddSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        basket = request.user.get_basket()
        item = get_object_or_404(Item, pk=serializer.data["item"])
        try:
            order_item = OrderItem.objects.get(order=basket, item=item)
            if serializer.data.get("quantity", 1) >= order_item.quantity:
                order_item.delete()
            else:
                order_item.quantity -= serializer.data.get("quantity", 1)
                order_item.save()
        except OrderItem.DoesNotExist:
            logger.error(f"Fail remove item from order {basket.id}")
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=OrderCompleteSerializer,
        responses={
            status.HTTP_200_OK: OrderCompleteSerializer,
        },
    )
    @action(detail=False, methods=["post"], url_name="complete")
    def complete_order(self, request):
        serializer = OrderCompleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            basket = request.user.get_basket()
            if basket.get_total_amount() == 0:
                logger.error(f"Fail complete empty basket {basket.id}")
                return Response(status=status.HTTP_400_BAD_REQUEST)
            basket.complete_order(serializer.data["payment_option"])

        except Exception:
            logger.error(f"Fail complete basket for user {request.user.id}")
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=UserVoucherIdSerializer,
        responses={
            status.HTTP_200_OK: UserVoucherShortSerializer,
        },
    )
    @action(detail=False, methods=["patch"], url_name="add-voucher")
    def add_voucher(self, request):
        serializer = UserVoucherIdSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_voucher = get_object_or_404(UserVoucher, pk=serializer.data["id"], is_active=True)
        try:
            basket = request.user.get_basket()
            basket.user_voucher = user_voucher
            user_voucher.is_active = False
            user_voucher.save()
            basket.save()

        except Exception:
            logger.error(f"Fail add voucher user {request.user.id}")
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: UserVoucherShortSerializer,
        },
    )
    @action(detail=False, methods=["patch"], url_name="remove-voucher")
    def remove_voucher(self, request):
        try:
            basket = request.user.get_basket()
            user_voucher = basket.user_voucher
            basket.user_voucher = None
            user_voucher.is_active = True
            user_voucher.save()
            basket.save()
        except Exception:
            logger.error(f"Fail remove voucher user {request.user.id}")
        return Response(status=status.HTTP_200_OK)
