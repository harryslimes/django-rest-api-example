# from django.conf.urls import url 
# from api import views 
 
# urlpatterns = [ 
#     url(r'^api/products$', views.product_list),
#     url(r'^api/products/<str:sku>/', views.product_detail),
#     url(r'^model/update-partial/<str:sku>/<int:amount_delta>/', views.product_amount),
#     url(r'^api/products/out_of_stock$', views.out_of_stock)
# ]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'products', views.ProductViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]