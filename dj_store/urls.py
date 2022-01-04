from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin
from .yasg import urlpatterns as dock_urls
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.routers import DefaultRouter
import store_api.views as st_wiews
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.documentation import include_docs_urls
from rest_framework_swagger.views import get_swagger_view

router = DefaultRouter()
router.register("", st_wiews.CategoryViewSet)

router2 = DefaultRouter()
router2.register("", st_wiews.AuthorViewSet)

API_TITLE = "Blog API"  # new
API_DESCRIPTION = "A Web API for creating and editing blog posts."  # new
# schema_view = get_schema_view(title=API_TITLE)  # new

schema_view = get_swagger_view(title=API_TITLE)

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
    # path("api/schema/", schema_view),
    path("api/docs/", include_docs_urls(title=API_TITLE, description=API_DESCRIPTION)),
    path('swagger/', schema_view),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += dock_urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""

curl -X POST -d "username=Admin&password=123admin123" http://127.0.0.1:8000/api/auth/token/

eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo5LCJ1c2VybmFtZSI6InlhcnlreWFyeWsiLCJleHAiOjE2Mzc0ODk4MjksImVtYWlsIjoieWFyeWt5YXJ5a0BnbWFpbC5jb20ifQ.dNvTZYRvRvlHxhIrVCctUXjfnmbMoFmuwwEqHK8afZ0

curl -H "Authorization: JWT <eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMCwidXNlcm5hbWUiOiJBZG1pbiIsImV4cCI6MTYzNzQ5NzE2OSwiZW1haWwiOiJkamFuZ29jb21tdW5pdHlweXRob24xMjNAZ21haWwuY29tIn0.EWBUzNdX2W6C2HlZ8HGpXUVEf98f8F9-ow_wYKZg5Is>" http://127.0.0.1:8000/api/comments/

"""
