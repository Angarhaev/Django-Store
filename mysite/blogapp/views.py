from django.shortcuts import render
from timeit import default_timer
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin,
                                        UserPassesTestMixin)
from django.views import View
from django.views.generic import (TemplateView,
                                  ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)
from django.contrib.auth.models import Group
from django.http import (HttpResponse,
                         HttpRequest,
                         HttpResponseRedirect,
                         JsonResponse)
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from .models import Author, Article, Tag, Category
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiResponse


class ArticleListView(ListView):
    template_name = 'blogapp/article_list.html'
    #model = Article
    queryset = (Article.objects.filter(pub_date__isnull=False)
                .order_by('-pub_date')
                .select_related('author', 'category')
                .prefetch_related('tags'))


class ArticleDetail(DetailView):
    model = Article
    template_name = 'blogapp/article_detail.html'
    context_object_name = 'article'
