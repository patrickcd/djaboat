from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.db import connection

from neapolitan.views import CRUDView

from . import models


def index(request):
    return render(request, "index.html", None)


class ItemView(CRUDView):
    model = models.Item
    fields = ["name", "notes", "location", "category", "weight_grams"]


class PassageView(CRUDView):
    model = models.Passage
    fields = ["date_start", "date_end", "destination", "origin", "distance"]


class MaintenanceView(CRUDView):
    model = models.Maintenance
    fields = [
        "task",
        "last_performed",
        "next_scheduled",
        "target_item",
        "category",
    ]
    filterset_fields = ["category"]
    order_fields = (("last_performed", "latest"), ("next_scheduled", "upcoming"))
    field_filters_map = {"task": lambda x: x[:50]}


class CategoryView(CRUDView):
    model = models.Category
    fields = ["name"]


class LocationView(CRUDView):
    model = models.Location
    fields = ["name", "cabin"]


class MaintenanceLogView(CRUDView):
    model = models.MaintenanceLog
    fields = ("maintenance", "date", "notes")


def search(request: HttpRequest) -> HttpResponse:
    termq = request.GET.get("boatq", default="")

    def queryify(terms):
        for token in terms.split():
            match token:
                case "or":
                    yield "OR"
                case "and":
                    yield "AND"
                case _:
                    yield f"{token}*"

    terms = " ".join(queryify(termq))
    rows = []
    if terms:
        stmt = "SELECT * FROM search_index WHERE object_text MATCH %s LIMIT 0,20"
        rows = None

        with connection.cursor() as cursor:  # type: ignore
            cursor.execute(stmt, [terms])
            columns = ["object_text", "object_id", "content_table"]
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return render(request, "search.html", {"rows": rows, "term": termq, "q": terms})
