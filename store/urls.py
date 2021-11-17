
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from store.views import Home_page

urlpatterns = [
    path("", Home_page.as_view(), name="home"),
]

