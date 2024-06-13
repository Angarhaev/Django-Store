from django.contrib.auth.views import LoginView
from django.urls import path
from .views import (AboutMeView,
                    MyLogoutView,
                    RegisterView,
                    set_cookies_view,
                    get_cookies_view,
                    set_session_view,
                    get_session_view)

app_name = 'myauth'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('about-me/', AboutMeView.as_view(), name='about_me'),
    path('login/', LoginView.as_view(
        template_name='myauth/login.html',
        redirect_authenticated_user=True
    ),
        name='login',
        ),
    path('logout/', MyLogoutView.as_view(), name='logout'),
    path('set_cookie/', set_cookies_view, name='set_cookie'),
    path('get_cookie/', get_cookies_view, name='get_cookie'),
    path('set_session/', set_session_view, name='set_session'),
    path('get_session/', get_session_view, name='get_session'),
]

