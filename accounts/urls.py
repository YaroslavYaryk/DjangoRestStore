from django.urls import path
from .views import UserCreateView, UserLoginView, UserLogin


urlpatterns = [
    path("register/", UserCreateView.as_view(), name="user_register"),
    path("login/", UserLoginView.as_view(), name="user_login"),
    path("token/login/", UserLogin.as_view(), name="token_login")
]
