from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
]

for crud_view in (
    views.ItemView,
    views.PassageView,
    views.MaintenanceView,
    views.LocationView,
    views.CategoryView,
    views.MaintenanceLogView,
):
    urlpatterns += crud_view.get_urls()
