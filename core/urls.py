from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path, include
from rest_framework import routers
from search.views import SearchProductInventory
from rest_api import views


router = routers.DefaultRouter()
router.register(
    r'api', views.AllProductsViewSet, basename="allproducts"
)
router.register(
    r'product', views.ProductInventoryViewSet, basename="products"
)
# router.register(
#     r'products-by-category/(?P<slug>[^/.]+)/$', views.ProductsByCategoryViewSet, basename='productsbycategory'
# )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('demo/', include("demo.urls", namespace="demo")),
    path('search/<str:query>/', SearchProductInventory.as_view()),
    path("api/", include(router.urls)),
    path("products-by-category/<path:hierarchy>/", views.ProductsByCategoryViewSet.as_view({'get': 'list'}), name="products-by-category"),
    # path('__debug__/', include('debug_toolbar.urls')),
    path('', include('inventory.urls')),

] + static(settings.IMAGES_STATIC_URL, document_root=settings.IMAGES_STATIC_ROOT)
