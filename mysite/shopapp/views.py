from timeit import default_timer

from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
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
    template_name = 'shopapp:product_list.html'
    #model = Product
    queryset = Product.objects.filter(archived=False)

class ProductDetailsView(DetailView):
    template_name = "shopapp/product_detail.html"
    #model = Product
    context_object_name = 'product'
    queryset = Product.objects.filter(archived=False)


class ProductCreate(CreateView):
    model = Product
    fields = ["name", "description", "price", "discount"]
    success_url = reverse_lazy("shopapp:products_list")


class ProductUpdate(UpdateView):
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


class OrdersListView(ListView):
    queryset = Order.objects.select_related("user").prefetch_related("products")


class OrderDetailView(DetailView):
    queryset = Order.objects.select_related("user").prefetch_related("products")


class OrderCreate(CreateView):
    model = Order
    fields = ["delivery_address", "promocode", "user", "products"]
    success_url = reverse_lazy("shopapp:orders_list")


class OrderUpdate(UpdateView):
    model = Order
    fields = ["delivery_address", "promocode", "user", "products"]
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse("shopapp:order_detail", kwargs={"pk": self.object.pk})


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy("shopapp:orders_list")

