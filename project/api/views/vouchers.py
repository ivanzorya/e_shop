from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from api.serializers import UserVoucherSerializer
from e_shop.models import UserVoucher


class UserVoucherViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = UserVoucher.objects.all()
    serializer_class = UserVoucherSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = self.request.user.uservoucher_set.filter(is_active=True)
            return queryset
        return []
