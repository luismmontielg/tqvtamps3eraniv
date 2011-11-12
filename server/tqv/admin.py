__author__ = 'luismmontielg'
from django.contrib import admin

from tqv.models import Activity, EventDetails

class ActivityAdmin(admin.ModelAdmin):
    model = Activity
    list_display = ('__unicode__', 'start_time', 'end_time',)
    search_fields = ['name', 'description']
    list_filter = ('enabled',)

class EventDetailsAdmin(admin.ModelAdmin):
        model = EventDetails
        list_display = ('__unicode__',)
        list_filter = ('event',)

admin.site.register(EventDetails, EventDetailsAdmin)
admin.site.register(Activity, ActivityAdmin)