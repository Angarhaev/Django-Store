from django.contrib.auth import logout
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View


class MyLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('myauth:login')


def set_cookies_view(request: HttpRequest):
    response = HttpResponse("Cookie set")
    response.set_cookie('fizz', 'buzz', max_age=3600)
    return response


def get_cookies_view(request: HttpRequest):
    value = request.COOKIES.get("fizz", "default")
    return HttpResponse(f"Cookie value: {value}")


def set_session_view(request: HttpRequest):
    request.session['Hello'] = "World!"
    return HttpResponse("Session set")


def get_session_view(request: HttpRequest):
    value = request.session.get("Hello", "default")
    return HttpResponse(f'Session value: {value}')
