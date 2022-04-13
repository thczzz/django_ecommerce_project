from django.contrib import admin
from .models import Category, Product, ProductInventory, ProductAttribute, ProductAttributeValue,\
    ProductAttributeValues, Media, Stock, Brand
from mptt.admin import MPTTModelAdmin

admin.site.register(Category, MPTTModelAdmin)
admin.site.register(Product)
admin.site.register(Brand)
admin.site.register(ProductInventory)
admin.site.register(ProductAttribute)
admin.site.register(ProductAttributeValue)


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    raw_id_fields = ["product_inventory"]


@admin.register(ProductAttributeValues)
class ProductAttributeValuesAdmin(admin.ModelAdmin):

    raw_id_fields = ["attributevalues", "productinventory"]


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    raw_id_fields = ["product_inventory"]
