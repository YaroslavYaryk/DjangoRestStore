from django.urls import path
from store.views import Home_page

urlpatterns = [
    path("", Home_page.as_view(), name="home"),
]
