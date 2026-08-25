from django.contrib import admin

from .models import Road


@admin.register(Road)
class RoadAdmin(admin.ModelAdmin):
    list_display = ('id', 'prefecture', 'section_number', 'route_name', 'section_length', 'total_traffic')
    list_filter = ('prefecture', 'route_name')
    search_fields = ('route_name', 'start_point', 'end_point')
    ordering = ('prefecture', 'section_number')
