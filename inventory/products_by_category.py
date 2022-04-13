from itertools import chain
from inventory.models import Product, Category


def get_products_by_category(hierarchy=None):
    products = Product.objects.all()
    selected_categories = []

    if hierarchy is not None:
        hierarchy = hierarchy.split('/')
        if len(hierarchy) > 1:
            last_el_slug = hierarchy[-1]
            last_el = Category.objects.filter(slug=last_el_slug).first()
            if last_el.is_leaf_node():
                products = products.filter(category__slug=last_el_slug)
            else:
                children = last_el.get_descendants(include_self=True)
                selected_categories.append(children)
                products = products.filter(category__in=children)
            parents = last_el.get_ancestors(include_self=True)
            selected_categories = list(chain(parents))
        else:
            last_el_slug = hierarchy[0]
            last_el = Category.objects.filter(slug=last_el_slug)[0]

            selected_categories.append(last_el)

            children = last_el.get_descendants(include_self=True)
            products = products.filter(category__in=children)

    products_count = products.count()
    products_to_return = products.order_by('-created_at')

    return (products_count, products_to_return, selected_categories)


def load_more(queryset, current):
    limit = 12
    products_to_return = queryset[current:current+limit]

    return products_to_return
