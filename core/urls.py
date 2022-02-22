from django.contrib import admin
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
router.register(
    r'products-by-category/(?P<slug>[^/.]+)', views.ProductInventoryViewSet, basename='productsbycategory'
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('demo/', include("demo.urls", namespace="demo")),
    path('search/<str:query>/', SearchProductInventory.as_view()),
    path("", include(router.urls)),
    path('__debug__/', include('debug_toolbar.urls')),
]
