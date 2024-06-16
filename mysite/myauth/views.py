from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView

from myauth.models import Profile


class AboutMeView(TemplateView):
    template_name = 'myauth/about-me.html'


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'myauth/register.html'
    success_url = reverse_lazy('myauth:about_me')

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(
            self.request,
            username=username,
            password=password
        )
        login(request=self.request, user=user)
        return response


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


def get_json(request: HttpRequest) -> JsonResponse:
    return JsonResponse({'foo': "bar", 'spam': "egg"})

