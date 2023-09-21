from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # 단순히 django.conrtib.auth의 login/logout 활용
    # 웹브라우저 상에서 API 테스트 할 때의 편의성을 위함
    path("api-auth/", include("rest_framework.urls")),
    path("", include("instagram.urls")),
]
