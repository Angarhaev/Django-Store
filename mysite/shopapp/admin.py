from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse

from shopapp.models import Product, Order
from shopapp.admin_mixins import ExportAsCSVMixin


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

    def get_queryset(self, request):   #для быстрой подгрузки из бд одним запросом
        return Order.objects.select_related("user").prefetch_related("products")

    def user_verbose(self, obj: Order) -> str:
        return obj.user.first_name or obj.user.username






