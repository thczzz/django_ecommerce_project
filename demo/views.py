from django.shortcuts import render
from django.db.models import Count
from django.contrib.postgres.aggregates import ArrayAgg
from inventory import models
from search.documents import ProductInventoryDocument


def home(request):
    return render(request, "index.html")


def category(request):
    data = models.Category.objects.all()

    return render(request, "categories.html", {"data": data})


def product_by_category(request, category):
    data = models.Product.objects.filter(category__name=category).values(
        "id", "name", "slug", "category__name", "product__store_price", "product__product_inventory__units"
    )
    print(data)
    return render(request, 'product_by_category.html', {'data': data})


def product_detail(request, slug):
    filter_arguments = []

    # If there are values, ex: ?color=red&shoe-size=5
    if request.GET:
        for value in request.GET.values():
            filter_arguments.append(value)

        data = models.ProductInventory.objects.filter(product__slug=slug).filter(
            attribute_values__attribute_value__in=filter_arguments).annotate(
            num_tags=Count('attribute_values')).filter(num_tags=len(filter_arguments)).values(
            "id", "sku", "product__name", "store_price", "product_inventory__units"
        ).annotate(attr_vals=ArrayAgg("attribute_values__attribute_value")).get()
    else:
        data = models.ProductInventory.objects.filter(product__slug=slug).filter(is_default=True).values(
            "id", "sku", "product__name", "store_price", "product_inventory__units"
        ).annotate(attr_vals=ArrayAgg("attribute_values__attribute_value")).get()

    y = models.ProductInventory.objects.filter(product__slug=slug).distinct().values(
        "attribute_values__product_attribute__name", "attribute_values__attribute_value")

    z = models.ProductTypeAttribute.objects.filter(
                      product_type__product_type__product__slug=slug).values("product_attribute__name").distinct()
# ProductTypeAttribute -> ProductType -> ProductInventory -> Product || ProductTypeAttribute -> ProductAttribute

    return render(request, "product_detail.html", {'data': data, 'product_type_attrs': z, 'product_attrs_values': y})


def elasticsearch_examples():
    e = ProductInventoryDocument.search().query("match", product__name="sneakers")
