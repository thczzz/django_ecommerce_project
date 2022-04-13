from django.contrib.postgres.aggregates import ArrayAgg
from django.http import JsonResponse
from django.shortcuts import render
from itertools import chain
from inventory import models
from inventory.products_by_category import get_products_by_category, load_more
from django.db.models import Count, Min
from django.template.loader import render_to_string

# Create your views here.


def home(request):
    top_brands = models.Brand.objects.prefetch_related('brand').annotate(
        num_of_products=Count("brand")
    ).order_by('-num_of_products')[:10]
    products = models.Product.objects.all().order_by('-created_at')
    categories_list = models.Category.objects.all()
    products = products.annotate(
        min_price=Min('product__retail_price')
    )

    context = {
        'top_brands': top_brands,
        'categories_list': categories_list,
    }

    if request.GET:
        request_keys = request.GET.keys()

        """
        Filter products by: brand, color, min_price, max_price, clothes size, shoe size
        Add filter_kwargs to the context for persistent filtering if user wants to sort the products.
        """
        if "fs_color_froup" in request_keys or "fs_size_group" in request_keys or "shoe_size_group" \
                        "min" in request_keys or "max" in request_keys or "brand" in request_keys:
            products = perform_filter(request, products)
            filter_kwargs = dict(request.GET)
            context["filter_kwargs"] = filter_kwargs

        """
        Sort products by: date added, price asc., price desc.
        Add sort_method to the context
        """
        sort_method = request.GET.get("sort", None)
        if sort_method is not None:
            if sort_method == "3":
                products = products.order_by('min_price')
            elif sort_method == "4":
                products = products.order_by('-min_price')
            elif sort_method == "2":
                products = products.order_by('-created_at')
            context["sort_method"] = sort_method

        """
        GET products (AJAX req.)
        """
        current = request.GET.get("current", None)
        if current is not None:
            html = perform_load_more(current, products=products)
            response = [html]
            if int(current) == 0:
                products_count = products.count()
                response.append(products_count)
            return JsonResponse(response, safe=False)

        """
        GET variants for product quickview
        """
        get_variants_for_quick_view = request.GET.get("get_variants_etc", None)
        if get_variants_for_quick_view is not None:
            obj = models.ProductInventory.objects.get(sku=get_variants_for_quick_view)
            variant_etc = get_variant_etc(obj=obj)
            html = render_to_string("partial/sizeLis.html", {'variant_etc': variant_etc})
            return JsonResponse(html, safe=False)

    return render(request, 'home.html', context)


def get_variant_etc(obj):
    """
    GET product variants (size, material, etc..)
    """

    sizes = obj.attribute_values.values(
        "product_attribute__name",
        "attribute_value",
    ).distinct(
        "product_attribute__name",
        "attribute_value",
    )
    attr_names_values_dict = {}
    attr_names_values = list(filter(lambda x: x["product_attribute__name"] != 'color', sizes))

    for obj in attr_names_values:
        if not obj["product_attribute__name"] in attr_names_values_dict:
            attr_names_values_dict[obj["product_attribute__name"]] = []
        if obj["attribute_value"] not in attr_names_values_dict[obj["product_attribute__name"]]:
            attr_names_values_dict[obj["product_attribute__name"]].append(obj["attribute_value"])

    return attr_names_values_dict
