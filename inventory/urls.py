from django.urls import path

from neapolitan.views import CRUDView

from . import views, models

class ItemView(CRUDView):
    model = models.Item
    fields = ['name', 'notes', 'location', 'category', 'weight_grams']


class PassageView(CRUDView):
    model = models.Passage
    fields = ['date_start', 'date_end', 'destination', 'origin', 'distance']

class MaintenanceView(CRUDView):
    model = models.Maintenance
    fields = ['task', 'recurrence', 'last_performed', 'item']

urlpatterns = [
    path("", views.index, name="index"),
    path("clicked", views.clicked, name="clicked"),
]

for crud_view in (ItemView, PassageView, MaintenanceView):
    urlpatterns += crud_view.get_urls()

