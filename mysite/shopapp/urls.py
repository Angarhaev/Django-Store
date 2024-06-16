from django.urls import path
from .views import (ShopIndexViews,
                    GroupsListView,
                    ProductsList,
                    ProductDetailsView,
                    ProductCreate,
                    ProductUpdate,
                    ProductArchiveView,
                    OrdersListView,
                    OrderDetailView,
                    OrderCreate,
                    OrderUpdate,
                    OrderDeleteView,
                    OrderExportJson)


app_name = 'shopapp'

urlpatterns = [
    path("", ShopIndexViews.as_view(), name="index"),
    path("groups/", GroupsListView.as_view(), name="groups"),
    path("products/", ProductsList.as_view(), name="products_list"),
    path("products/create", ProductCreate.as_view(), name="product_create"),
    path("products/<int:pk>", ProductDetailsView.as_view(), name="product_detail"),
    path("products/<int:pk>/update", ProductUpdate.as_view(), name="product_update"),
    path("products/<int:pk>/delete", ProductArchiveView.as_view(), name="product_archive"),
    path("orders/", OrdersListView.as_view(), name="orders_list"),
    path("orders/create", OrderCreate.as_view(), name="order_create"),
    path("order/<int:pk>", OrderDetailView.as_view(), name="order_detail"),
    path("order/<int:pk>/update", OrderUpdate.as_view(), name="order_update"),
    path("order/<int:pk>/delete", OrderDeleteView.as_view(), name="order_delete"),
    path("order/export", OrderExportJson.as_view(), name='order_export')
]