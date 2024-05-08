from timeit import default_timer
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render


def shop_index(request: HttpRequest):
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