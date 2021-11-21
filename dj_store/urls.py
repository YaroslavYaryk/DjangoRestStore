"""dj_store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin
from .yasg import urlpatterns as dock_urls
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.routers import DefaultRouter
from store_api.views import CategoryViewSet, AuthorViewSet

router = DefaultRouter()
router.register('', CategoryViewSet)

router2 = DefaultRouter()
router2.register('', AuthorViewSet)



urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("api/", include("store_api.urls")),
    path("api/accounts/", include("accounts.urls")),
    path("api/comments/", include("comments.urls")),
    path("", include("store.urls")),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
    path("auth/", include("djoser.urls.jwt")),
    path("api/rest-auth/", include("rest_auth.urls")),
    path("api/rest-auth/registration/", include("rest_auth.registration.urls")),
    path("api/auth/token/", obtain_jwt_token),
    path("api/category/", include(router.urls)),
    path("api/author/", include(router2.urls)),

]

urlpatterns += dock_urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


"""

curl -X POST -d "username=Admin&password=123admin123" http://127.0.0.1:8000/api/auth/token/

eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo5LCJ1c2VybmFtZSI6InlhcnlreWFyeWsiLCJleHAiOjE2Mzc0ODk4MjksImVtYWlsIjoieWFyeWt5YXJ5a0BnbWFpbC5jb20ifQ.dNvTZYRvRvlHxhIrVCctUXjfnmbMoFmuwwEqHK8afZ0

curl -H "Authorization: JWT <eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMCwidXNlcm5hbWUiOiJBZG1pbiIsImV4cCI6MTYzNzQ5NzE2OSwiZW1haWwiOiJkamFuZ29jb21tdW5pdHlweXRob24xMjNAZ21haWwuY29tIn0.EWBUzNdX2W6C2HlZ8HGpXUVEf98f8F9-ow_wYKZg5Is>" http://127.0.0.1:8000/api/comments/

"""
