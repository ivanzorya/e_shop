from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views.favorites import FavoritesViewSet
from api.views.items import ItemViewSet
from api.views.orders import OrderViewSet
from api.views.users import UserViewSet
from api.views.vouchers import UserVoucherViewSet

router = routers.DefaultRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"items", ItemViewSet, basename="items")
router.register(r"orders", OrderViewSet, basename="orders")
router.register(r"favorites", FavoritesViewSet, basename="favorites")
router.register(r"vouchers", UserVoucherViewSet, basename="vouchers")


urlpatterns = [
    path("", include(router.urls)),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
]
