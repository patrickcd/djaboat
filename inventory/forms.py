from django import forms

from .models import Item, Maintenance


class FKLookupWidget(forms.Select):
    template_name = "fklookup.html"


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = [""]
        widgets = {
            "name": forms.Textarea(attrs={"cols": 80, "rows": 20}),
            "category": FKLookupWidget(),
        }


class MainteanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        exclude = [""]
