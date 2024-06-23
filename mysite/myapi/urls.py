from django.urls import path

from myapi.views import hello_world, APIGroups

app_name = 'myapi'

urlpatterns = [
    path('hello/', hello_world, name='hello'),
    path('groups', APIGroups.as_view(), name='groups')
]
