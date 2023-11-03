from django import forms

from .models import Item, Maintenance, Location


class FKLookupWidget(forms.Select):
    template_name = "fklookup.html"


class FKAddNewWidget(forms.Select):
    template_name = "fk_add_new.html"


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = [""]
        widgets = {
            "notes": forms.Textarea(attrs={"cols": 80, "rows": 20}),
            "location": FKAddNewWidget(),
        }


class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        exclude = [""]
        widgets = {
            "target_item": FKLookupWidget(attrs={"content_type": "item"}),
        }


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        exclude = [""]


class ItemLocationsForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["location"]
