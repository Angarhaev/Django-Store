from timeit import default_timer

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy

from .forms import GroupForm
from .models import Product, Order


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
    permission_required = ['shopapp.view_order']
    queryset = Order.objects.select_related("user").prefetch_related("products")


class OrderDetailView(UserPassesTestMixin, DetailView):
    def test_func(self):
        order = self.get_object()
        creator = order.user
        return self.request.user.is_superuser or self.request.user == creator

    queryset = Order.objects.select_related("user").prefetch_related("products")


class OrderCreate(LoginRequiredMixin, CreateView):
    model = Order
    fields = ["delivery_address", "promocode", "user", "products"]
    success_url = reverse_lazy("shopapp:orders_list")


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
    success_url = reverse_lazy("shopapp:orders_list")


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

