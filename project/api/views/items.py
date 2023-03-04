from rest_framework import mixins, viewsets

from api.serializers import ItemSerializer
from e_shop.models import Item


class ItemViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
