from rest_framework import serializers
from inventory.models import Product, ProductInventory, Brand, ProductAttributeValue, Media, Stock, ProductAttribute


class MediaSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Media
        fields = ("image", "alt_text")
        read_only = True

    def get_image(self, obj):
        return self.context["request"].build_absolute_uri(obj.image.url)


class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        exclude = ('id',)


class ProductAttributeValueSerializer(serializers.ModelSerializer):
    product_attribute = ProductAttributeSerializer(many=False, read_only=True)

    class Meta:
        model = ProductAttributeValue
        exclude = ("id",)


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ("name",)


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ("units",)


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('name', 'slug',)
        read_only = True
        editable = False


class ProductInventorySerializer(serializers.ModelSerializer):
    brand = BrandSerializer(many=False, read_only=True)
    attributes = ProductAttributeValueSerializer(source="attribute_values", many=True, read_only=True)
    image = MediaSerializer(source="media_product_inventory", many=True)
    product = ProductSerializer(many=False, read_only=True)

    class Meta:
        model = ProductInventory
        fields = (
            "product",
            "sku",
            "store_price",
            "is_default",
            "image",
            "product_type",
            "brand",
            "attributes"
        )
        read_only = True


# class ProductInventorySerializer(serializers.ModelSerializer):
#     product = ProductSerializer(many=False, read_only=True)
#     product_inventory = StockSerializer(many=False, read_only=True)
#
#     class Meta:
#         model = ProductInventory
#
#         fields = (
#             "id", 'product', "sku", "store_price", "is_default", "product_inventory"
#         )
#         read_only = True
