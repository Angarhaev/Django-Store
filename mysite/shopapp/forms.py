from django import forms
from django.forms import ModelForm

from .models import Product, Order
from django.contrib.auth.models import Group


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ["name"]
