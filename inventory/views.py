from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.db import connection
from django.utils.text import Truncator

from neapolitan.views import CRUDView

from . import models, forms


def _truncate(long_text):
    truncator = Truncator(long_text)
    return truncator.words(8)


def index(request):
    return render(request, "index.html", None)


class ItemView(CRUDView):
    model = models.Item
    form_class = forms.ItemForm
    fields = ["name", "location", "category"]
    detail_fields = [
        "name",
        "notes",
        "location",
        "category",
        "item_type",
        "weight_grams",
        "extra",
    ]


class ItemTypeView(CRUDView):
    model = models.ItemType
    fields = ["name", "properties"]


class PassageView(CRUDView):
    model = models.Passage
    fields = ["date_start", "date_end", "destination", "origin", "distance"]


class MaintenanceView(CRUDView):
    model = models.Maintenance
    form_class = forms.MaintenanceForm
    fields = [
        "task",
        "last_performed",
        "next_scheduled",
        "target_item",
        "category",
    ]
    filterset_fields = ["category"]
    order_fields = (
        ("last_performed", "last_performed"),
        ("next_scheduled", "next_scheduled"),
    )
    field_filters_map = {"task": _truncate}


class CategoryView(CRUDView):
    model = models.Category
    fields = ["name"]


class LocationView(CRUDView):
    model = models.Location
    fields = ["name", "cabin"]


class MaintenanceLogView(CRUDView):
    model = models.MaintenanceLog
    fields = ("maintenance", "date", "notes")


def search(request: HttpRequest):
    termq = request.GET.get("boatq", default="")
    content_type = request.GET.get("content_type", None)

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
        stmt_args = [terms]
        stmt = "SELECT * FROM search_index WHERE object_text MATCH %s "
        if content_type:
            db_table = f"inventory_{content_type}"
            stmt += " AND content_table = %s"
            stmt_args.append(db_table)
        stmt += " LIMIT 0,20"
        rows = None

        with connection.cursor() as cursor:  # type: ignore
            cursor.execute(stmt, stmt_args)
            columns = ["object_text", "object_id", "content_table"]
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

    if "application/json" in request.META["HTTP_ACCEPT"].lower():
        return JsonResponse(rows, safe=False)
    else:
        return render(request, "search.html", {"rows": rows, "term": termq, "q": terms})


def add_new_location(request: HttpRequest):
    if request.method == "GET":
        location_form = forms.LocationForm()
        return render(request, "partials/new_location.html", {"form": location_form})
    if request.method == "POST":
        form = forms.LocationForm(request.POST)
        if form.is_valid():
            form.save()
            item_location_form = forms.ItemLocationsForm()
            return render(request, "partials/field.html", {"form": item_location_form})
