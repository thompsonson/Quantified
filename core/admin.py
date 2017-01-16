from django.contrib import admin
from .models import SleepAs, aTimeLogger

# Register your models here.


class SleepAsAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    exclude = 'sleep_data'

admin.site.register(SleepAs)


class aTimeLoggerAdmin(admin.ModelAdmin):
    date_hierarchy = 'start_time'

admin.site.register(aTimeLogger)
