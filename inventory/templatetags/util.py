from django import template
from django.urls import reverse
from django.forms import ModelForm, BoundField
from django.db.models.options import Options

register = template.Library()


@register.filter
def get_type(value):
    return type(value)


@register.filter
def searchlink(search_hit: dict) -> str:
    model_name = search_hit["content_table"].split("_")[1]
    return reverse(f"{model_name}-detail", kwargs={"pk": search_hit["object_id"]})


class ModelFormInspector:
    def __init__(self, model_form: ModelForm) -> None:
        self.form = model_form
        self.model_meta: Options = model_form.Meta.model._meta

    def field_is_related(self, field: BoundField):
        model_field = self.model_meta.get_field(field.name)
        return model_field.is_relation


@register.filter
def is_related(field):
    mfi = ModelFormInspector(field.form)
    return mfi.field_is_related(field)
