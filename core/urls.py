from django.contrib import admin
from django.urls import include, path
from rest_framework_jwt.views import (
    obtain_jwt_token,
    refresh_jwt_token,
    verify_jwt_token,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # 단순히 django.conrtib.auth의 login/logout 활용
    # 웹브라우저 상에서 API 테스트 할 때의 편의성을 위함
    path("api-auth/", include("rest_framework.urls")),
    path("accounts/", include("accounts.urls")),
    path("", include("instagram.urls")),
    path("api-jwt-auth/", obtain_jwt_token),
    path("api-jwt-auth/refresh/", refresh_jwt_token),
    path("api-jwt-auth/verify/", verify_jwt_token),
]
