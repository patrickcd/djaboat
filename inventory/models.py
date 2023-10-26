from django.db import models
from django.urls import reverse


class UrlMixin:
    def get_absolute_url(self):
        view_name = f"{self._meta.model_name}-detail"  # type: ignore
        return reverse(view_name, kwargs={"pk": self.pk})  # type: ignore


class Location(models.Model, UrlMixin):
    name = models.CharField(max_length=200)
    cabin = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Category(models.Model, UrlMixin):
    class Meta:
        verbose_name_plural = "categories"

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Documents(models.Model, UrlMixin):
    title = models.CharField(max_length=100)
    document = models.JSONField()


class Item(models.Model, UrlMixin):
    name = models.CharField(max_length=200)
    notes = models.TextField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    weight_grams = models.IntegerField(default=0)
    document = models.ForeignKey(
        Documents, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.name


class Maintenance(models.Model, UrlMixin):
    class Meta:
        verbose_name_plural = "maintenance tasks"
        verbose_name = "maintenance task"

    task = models.CharField(max_length=200)
    recurrence = models.CharField(max_length=100)
    last_performed = models.DateField(null=True, default=None, blank=True)
    next_scheduled = models.DateField(null=True, default=None, blank=True)
    target_item = models.ForeignKey(
        Item, null=True, blank=True, on_delete=models.CASCADE
    )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    requires_items = models.ManyToManyField(Item, related_name="used_for")

    def __str__(self):
        return self.task


class MaintenanceLog(models.Model, UrlMixin):
    maintenance = models.ForeignKey(Maintenance, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField()
    notes = models.TextField()

    def __str__(self):
        return (
            f"Log Entry for {self.maintenance.task} on {self.date.strftime('%d %b %Y')}"
        )


class Passage(models.Model, UrlMixin):
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    destination = models.CharField(max_length=200)
    origin = models.CharField(max_length=200)
    distance = models.DecimalField(max_digits=5, decimal_places=1)

    def __str__(self):
        return f"{self.origin} to {self.destination} on {self.date_start}"


class Waypoint(models.Model, UrlMixin):
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    time = models.DateTimeField(auto_now_add=True)
    passage = models.ForeignKey(Passage, on_delete=models.SET_NULL, null=True)
    wind_speed = models.IntegerField()
    wind_direction = models.IntegerField()
