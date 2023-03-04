from django.contrib import admin

from e_shop.models import Item, Order, OrderItem, UserVoucher, Voucher

admin.site.register(Item)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Voucher)
admin.site.register(UserVoucher)
