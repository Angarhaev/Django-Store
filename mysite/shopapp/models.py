from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from myauth.models import Profile


class Product(models.Model):
    class Meta:
        ordering = ["name", "price"]
        # db_table = "tech_products"
        verbose_name = _('Product')
        verbose_name_plural = _("Products")

    name = models.CharField(max_length=100)
    description = models.TextField(null=False, blank=True)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    discount = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None)
    archived = models.BooleanField(default=False)


    def __str__(self) -> str:
        return f"Product(pk={self.pk}, name={self.name!r})"


class Order(models.Model):
    class Meta:
        #ordering = [""]
        # db_table = "orders"
        verbose_name = _('Order')
        verbose_name_plural = _("Orders")
    delivery_address = models.TextField(null=True, blank=True)
    promocode = models.CharField(max_length=20, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name='orders')


