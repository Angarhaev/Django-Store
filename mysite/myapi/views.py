from django.contrib.auth.models import Group
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from myapi.serialized import GroupSerialize


@api_view()
def hello_world(request: Request) -> Response:
    return Response({'message': 'Hello World!'})


class APIGroups(ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerialize
    