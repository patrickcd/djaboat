from django.contrib import admin
from .models import (
    Item,
    Location,
    Category,
    Maintenance,
    MaintenanceLog,
    Passage,
    Waypoint,
    ItemType,
)


class ItemAdmin(admin.ModelAdmin):
    pass


class LocationAdmin(admin.ModelAdmin):
    pass


class CategoryAdmin(admin.ModelAdmin):
    pass


class MaintenanceAdmin(admin.ModelAdmin):
    pass


class MaintenanceLogAdmin(admin.ModelAdmin):
    pass


class PassageAdmin(admin.ModelAdmin):
    pass


class WaypointAdmin(admin.ModelAdmin):
    pass


class ItemTypeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Item, ItemAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Maintenance, MaintenanceAdmin)
admin.site.register(MaintenanceLog, MaintenanceLogAdmin)
admin.site.register(Passage, PassageAdmin)
admin.site.register(Waypoint, WaypointAdmin)
admin.site.register(ItemType, ItemTypeAdmin)
