"""
Модуль представлений над заказами и товарами.

В этом модуле содержаться различные представления для работы
с заказами и товарами.
"""

from timeit import default_timer
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin,
                                        UserPassesTestMixin)
from django.contrib.syndication.views import Feed
from django.core.cache import cache
from django.views import View
from django.views.generic import (TemplateView,
                                  ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)
from django.contrib.auth.models import Group, User
from django.http import (HttpResponse,
                         HttpRequest,
                         HttpResponseRedirect,
                         JsonResponse)
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from .forms import GroupForm
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiResponse
import logging


log = logging.getLogger(__name__)


class LatestProductFeed(Feed):
    title = "Products latest"
    description = "Updates on changes and additional products"
    link = reverse_lazy('shopapp:products_list')

    def items(self):
        return Product.objects.filter(archived=False).order_by('-created_at')

    def item_title(self, item: Product):
        return item.name if item.name else 'no name'

    def item_description(self, item: Product):
        return item.description[:30] if item.description else 'no description'

    def item_pubdate(self, item: Product):
        return item.created_at

    def item_link(self, item: Product):
        return item.get_absolute_url()


@extend_schema(description="Product Views CRUD")
class ProductViewSet(ModelViewSet):
    """
    Набор представлений для действий над Product.

    Полный CRUD для сущностей товара.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = ['name', 'description']
    filterset_fields = ['name', 'description', 'price', 'discount', 'archived']
    ordering_fields = ['name', 'price', 'discount']

    @extend_schema(summary='Get 1 product by id',
                   description="Retrieves product, returns 404 if not found",
                   responses={
                       "200": ProductSerializer,
                       "404": OpenApiResponse(description='Empty response'),
                              })
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter
    ]
    search_fields = ['delivery_address', 'promocode']
    filterset_fields = ['id', 'delivery_address', 'promocode']
    ordering_fields = ['id', 'delivery_address', 'promocode']


class ShopIndexViews(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        products = [
            ('laptop', 500),
            ('desktop', 700),
            ('mouse', 50),
            ('keyboard', 70),
            ('smartphone', 150),
         ]
        context = {
            "time_running": default_timer(),
            "products": products
        }
        #logging.info('Products for shop index %s', products)
        return render(request, 'shopapp/shop-index.html', context=context)


class GroupsListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "groups": Group.objects.prefetch_related('permissions').all(),
            "form": GroupForm()
        }
        return render(request, "shopapp/groups.html", context=context)

    def post(self, request: HttpRequest):
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(request.path)


class ProductsList(ListView):
    template_name = 'shopapp/product_list.html'
    #model = Product
    queryset = Product.objects.filter(archived=False)


class ProductDetailsView(UserPassesTestMixin, DetailView):
    def test_func(self):
        product = self.get_object()
        creator = product.created_by
        return self.request.user.is_superuser or self.request.user == creator

    template_name = "shopapp/product_detail.html"
    #model = Product
    context_object_name = 'product'
    queryset = Product.objects.filter(archived=False)


class ProductCreate(PermissionRequiredMixin, CreateView):
    permission_required = ['shopapp.add_product']
    model = Product
    fields = ["name", "description", "price", "discount"]
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ProductUpdate(UserPassesTestMixin, PermissionRequiredMixin, UpdateView):
    def test_func(self):
        product = self.get_object()
        creator = product.created_by
        return self.request.user.is_superuser or self.request.user == creator

    permission_required = ['shopapp.change_product']
    model = Product
    fields = ["name", "description", "price", "discount"]
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse("shopapp:product_detail", kwargs={"pk": self.object.pk})


class ProductArchiveView(DeleteView):
    model = Product
    success_url = reverse_lazy("shopapp:products_list")
    template_name_suffix = "_confirm_archive"

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class OrdersListView(PermissionRequiredMixin, ListView):
    template_name = 'shopapp/order_list.html'
    permission_required = ['shopapp.view_order']
    queryset = Order.objects.select_related("user").prefetch_related("products")


class UserOrdersListView(UserPassesTestMixin, ListView):
    template_name = 'shopapp/user_order_list.html'
    queryset = Order.objects.select_related("user").prefetch_related("products")

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.id == self.kwargs['user_id']

    def get_queryset(self):
        id = self.kwargs['user_id']
        self.owner = get_object_or_404(User, id=id)
        return Order.objects.filter(user=self.owner)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owner'] = self.owner
        return context


class OrderDetailView(UserPassesTestMixin, DetailView):
    def test_func(self):
        order = self.get_object()
        creator = order.user
        return self.request.user.is_superuser or self.request.user == creator

    queryset = Order.objects.select_related("user").prefetch_related("products")


class OrderCreate(LoginRequiredMixin, CreateView):
    model = Order
    fields = ["delivery_address", "promocode", "user", "products"]

    def get_success_url(self):
        return reverse("shopapp:user_orders_list", kwargs={"user_id": self.object.user.pk})


class OrderUpdate(UserPassesTestMixin, UpdateView):
    def test_func(self):
        order = self.get_object()
        creator = order.user
        return self.request.user.is_superuser or self.request.user == creator

    model = Order
    fields = ["delivery_address", "promocode", "user", "products"]
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse("shopapp:order_detail", kwargs={"pk": self.object.pk})


class OrderDeleteView(UserPassesTestMixin, DeleteView):
    def test_func(self):
        order = self.get_object()
        creator = order.user
        return self.request.user.is_superuser or self.request.user == creator
    model = Order

    def get_success_url(self):
        return reverse("shopapp:user_orders_list", kwargs={"user_id": self.object.user.pk})


class OrderExportJson(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def get(self, request: HttpRequest) -> JsonResponse:
        orders = Order.objects.order_by("pk").all()
        orders_data = [
            {
                'pk': order.pk,
                'deliver_address': order.delivery_address,
                'promocode': order.promocode,
                'created_at': str(order.created_at),
                'user': order.user.username,
                'products': list(order.products.order_by('pk').all().values_list('name', flat=True))
            }
            for order in orders
        ]
        return JsonResponse({'orders': orders_data})


class UserOrderExportJson(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.id == self.kwargs['user_id']

    def get(self, request: HttpRequest, user_id) -> JsonResponse:
        cache_key = f'orders_export_{user_id}'
        orders_data = cache.get(cache_key)
        if orders_data is None:
            orders = Order.objects.select_related('user').filter(user__id=user_id).order_by('pk').all()
            serializer = OrderSerializer(orders, many=True)
            orders_data = serializer.data
            cache.set(cache_key, orders_data, 60)
        return JsonResponse({'orders': orders_data})
