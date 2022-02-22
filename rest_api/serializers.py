from rest_framework import serializers
from inventory.models import Product, ProductInventory, Brand, ProductAttributeValue, Media, Stock


class MediaSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Media
        fields = ("image", "alt_text")
        read_only = True

    def get_image(self, obj):
        return self.context["request"].build_absolute_uri(obj.image.url)


class ProductAttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttributeValue
        exclude = ("id",)
        depth = 2


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ("name",)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # exclude = ('created_at', 'updated_at')
        fields = ('name',)
        read_only = True
        editable = False


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ("units",)


# class ProductInventorySerializer(serializers.ModelSerializer):
#     brand = BrandSerializer(many=False, read_only=True)
#     attributes = ProductAttributeValueSerializer(source="attribute_values", many=True)
#     image = MediaSerializer(source="media_product_inventory", many=True)
#
#     class Meta:
#         model = ProductInventory
#         fields = (
#             "sku",
#             "store_price",
#             "is_default",
#             "image",
#             "product",
#             "product_type",
#             "brand",
#             "attributes"
#         )
#         read_only = True


class ProductInventorySerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False, read_only=True)
    product_inventory = StockSerializer(many=False, read_only=True)

    class Meta:
        model = ProductInventory

        fields = (
            "id", 'product', "sku", "store_price", "is_default", "product_inventory"
        )
        read_only = True
