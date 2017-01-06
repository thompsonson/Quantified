from django.contrib import admin
from .models import SleepAs

# Register your models here.


class SleepAsAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    exclude = 'sleep_data'


admin.site.register(SleepAs)
