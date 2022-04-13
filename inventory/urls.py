from django.urls import path
from inventory import views


urlpatterns = [
    path('', views.home, name='home'),
    path('shop/<path:hierarchy>/', views.shop, name='shop'),
    path('product/<str:slug>/', views.product_details, name='product-details')
]
