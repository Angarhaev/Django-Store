from django.urls import path
from .views import shop_index, groups, products_list, orders_list

app_name = 'shopapp'

urlpatterns = [
    path("", shop_index, name="index"),
    path("groups/", groups, name="groups"),
    path("products/", products_list, name="products_list"),
    path("orders/", orders_list, name="orders_list")
]