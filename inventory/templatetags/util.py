from django import template
from django.urls import reverse

register = template.Library()


@register.filter
def get_type(value):
    return type(value)


@register.filter
def searchlink(search_hit: dict) -> str:
    model_name = search_hit["content_table"].split("_")[1]
    return reverse(f"{model_name}-detail", kwargs={"pk": search_hit["object_id"]})
