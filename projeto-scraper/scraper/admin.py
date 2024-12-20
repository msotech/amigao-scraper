from django.contrib import admin
from .models import Store, URL, Product, History


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    pass


@admin.register(URL)
class URLAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'description', 'store')
    list_display = ('id', 'sku', 'description', 'store')
    search_fields = ('description',)


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    readonly_fields = ('product', 'at', 'default_price', 'offer_price', 'offer', 'category')
    list_display = ('product', 'default_price', 'offer_price', 'offer', 'at')
    list_filter = ('product__description', 'offer', 'at')
    search_fields = ('product__description',)
