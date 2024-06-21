from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views import View
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DetailView
from myauth.forms import ProfileForm, AvatarUpdateForm
from myauth.models import Profile



class HelloWorld(View):
    def get(self, request):
        text = _('welcome Hello World!')
        return HttpResponse(f'<h1>{text}</h1>')


class AboutMeRedirectView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        pk = self.request.user.pk
        return redirect(reverse_lazy('myauth:about_me_detail', kwargs={'pk': pk}))


class AboutMeView(UserPassesTestMixin, TemplateView):
    template_name = 'myauth/about_me.html'

    def test_func(self):
        if self.request.user.is_authenticated:
            profile_owner = self.get_object()
            return self.request.user.is_superuser or self.request.user == profile_owner.user
        else:
            return False

    def get_object(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        print(profile)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AvatarUpdateForm()#instance=self.request.user.profile)
        return context

    def post(self, request, pk):
        form = AvatarUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('myauth:about_me_detail', kwargs={'pk': pk}))


class ProfileDetail(DetailView):
    template_name = 'myauth/profile_detail.html'
    model = Profile
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AvatarUpdateForm()
        return context

    def post(self, request, pk):
        if self.request.user.is_staff or self.request.user == self.get_object().user:
            self.object = self.get_object()
            form = AvatarUpdateForm(request.POST, request.FILES, instance=self.object)
            if form.is_valid():
                form.save()
                return redirect(reverse_lazy('myauth:profile_detail', kwargs={'pk': self.object.pk}))
        else:
            return redirect(reverse_lazy('myauth:profile_detail', kwargs={'pk': self.get_object().pk}))


class ProfilesList(ListView):
    template_name = 'myauth/profile_list.html'
    queryset = Profile.objects.all()


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'myauth/register.html'
    success_url = reverse_lazy('myauth:about_me_redirect')

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

