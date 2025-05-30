from django.contrib import admin

from items.models import Discount, Item, Order, Tax


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    list_editable = ('price',)
    search_fields = ('name',)


@admin.register(Order)
class OrderItem(admin.ModelAdmin):
    list_display = ('__str__', 'items_amount')
    filter_vertical = ('items', 'discounts', 'taxes')
    readonly_fields = ('created_at',)

    @admin.display(description='Количество товаров')
    def items_amount(self, obj):
        return obj.items.count()


admin.site.register(Discount)
admin.site.register(Tax)
