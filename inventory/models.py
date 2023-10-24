from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=200)
    cabin = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Category(models.Model):
    class Meta:
        verbose_name_plural = "categories"

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=200)
    notes = models.TextField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    weight_grams = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Maintenance(models.Model):
    class Meta:
        verbose_name_plural = "maintenance tasks"

    task = models.CharField(max_length=200)
    recurrence = models.CharField(max_length=100)
    last_performed = models.DateTimeField(blank=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'Maintenance Task: {self.task}'


class MaintenanceLog(models.Model):
    maintenance = models.ForeignKey(Maintenance, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField()
    notes = models.TextField()


class Passage(models.Model):
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    destination = models.CharField(max_length=200)
    origin = models.CharField(max_length=200)
    distance = models.DecimalField(max_digits=5, decimal_places=1)

    def __str__(self):
        return f"{self.origin} to {self.destination} on {self.date_start}"


class Waypoint(models.Model):
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    time = models.DateTimeField(auto_now_add=True)
    passage = models.ForeignKey(Passage, on_delete=models.SET_NULL, null=True)
    wind_speed = models.IntegerField()
    wind_direction = models.IntegerField()

