from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path("", lambda req: redirect("/inventory/")),
    path("admin/", admin.site.urls),
    path("inventory/", include("inventory.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
]
