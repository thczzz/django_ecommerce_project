from django.shortcuts import render
from rest_framework import viewsets, mixins, permissions
from rest_framework.response import Response

from .serializers import ProductSerializer, ProductInventorySerializer
from inventory.models import Product, ProductInventory


class AllProductsViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin
):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "slug"

    def retrieve(self, request, slug=None):
        queryset = Product.objects.filter(category__slug=slug)[:10]
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)


class ProductInventoryViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = ProductInventory.objects.all()
    serializer_class = ProductInventorySerializer


class ProductsByCategoryViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = ProductInventory.objects.all()
    # serializer_class = ProductInventorySerializer

    """ 
    Get Items by category slug
    """
    def list(self, request, slug=None):
        queryset = ProductInventory.objects.filter(
            product__category__slug=slug,
        ).filter(is_default=True)[:10]
        serializer = ProductInventorySerializer(queryset, context={"request": request}, many=True)

        return Response(serializer.data)
