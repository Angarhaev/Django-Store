import re
from datetime import datetime

from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import path

from shopapp.models import Product, Order
from shopapp.admin_mixins import ExportAsCSVMixin
from shopapp.forms import CSVImportForm

from io import TextIOWrapper
from csv import DictReader


@admin.action(description="Archived products")
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)


@admin.action(description="Unarchived products")
def mark_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)


class ProductInline(admin.TabularInline):
    model = Order.products.through


class OrderInline(admin.TabularInline):
    model = Product.orders.through


@admin.register(Product)  #admin.site.register(Product, ProductAdmin) - аналог не декоратором
class ProductAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    ordering = "pk", #добавляет в отображении сотировку по primary key
    search_fields = "name", "price", "description",
    list_display = "pk", "name", "description_short", "price", "discount", "archived"
    list_display_links = "pk", "name" #для открытия как ссылки по записям данных столбцов
    inlines = [
        OrderInline,
    ]
    actions = [
        mark_archived,
        mark_unarchived,
        "export_csv"
    ]
    fieldsets = [
        (None, {
            "fields": ("name", "description"),
        }),
        ("Price options", {
            "fields": ("price", "discount"),
            "classes": ("wide",),
        }),
        ("Extra options", {
            "fields": ("archived",),
            "classes": ("collapse",),
            "description": "some description text",
        })
    ]


    def description_short(self, obj: Product) -> str:
        if len(obj.description) < 48:
            return obj.description
        return obj.description[:48] + '...'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = "delivery_address", "promocode", "created_at", "user_verbose"

    inlines = [
        ProductInline,
    ]

    change_list_template = 'shopapp/orders_changelist.html'

    def get_queryset(self, request):   #для быстрой подгрузки из бд одним запросом
        return Order.objects.select_related("user").prefetch_related("products")

    def user_verbose(self, obj: Order) -> str:
        return obj.user.first_name or obj.user.username

    def import_csv(self, request: HttpRequest) -> HttpResponse:
        if request.method == "GET":
            form = CSVImportForm()
            context = {
                'form': form,
            }
            return render(request, "admin/csv_form.html", context)

        form = CSVImportForm(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                'form': form
            }
            return render(request, "admin/csv_form.html", context, status=400)

        csv_file = TextIOWrapper(
            form.files['csv_file'].file,
            encoding=request.encoding
        )

        reader = DictReader(csv_file)

        for row in reader:
            delivery_address = row['delivery_address']
            promocode = row['promocode']
            created_at = row['created_at']
            user = User.objects.get(pk=row['user'])
            products_list = list(map(int, re.findall(r'\d+', row['products'])))
            order = Order(
                delivery_address=delivery_address,
                promocode=promocode,
                created_at=created_at,
                user=user,
            )

            order.save()
            products = Product.objects.filter(id__in=products_list)
            order.products.set(products)


        self.message_user(request, "Orders data from CSV was imported")
        return redirect('..')

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path('import-order-csv/',
                 self.import_csv,
                 name='import_orders_csv')
        ]
        return new_urls + urls






