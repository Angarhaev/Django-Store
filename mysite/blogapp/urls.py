from django.urls import path
from .views import ArticleListView, ArticleDetail


app_name = 'blogapp'

urlpatterns = [
    path('articles/', ArticleListView.as_view(), name='article_list'),
    path('article/<int:pk>', ArticleDetail.as_view(), name='article_detail'),
]
