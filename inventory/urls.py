from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("partials/add-new-location", views.add_new_location, name="add-new-location"),
]

for crud_view in (
    views.ItemView,
    views.ItemTypeView,
    views.PassageView,
    views.MaintenanceView,
    views.LocationView,
    views.CategoryView,
    views.MaintenanceLogView,
):
    urlpatterns += crud_view.get_urls()
