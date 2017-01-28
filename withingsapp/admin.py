# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import WithingsUser, MeasureGroup, Measure

# Register your models here.

admin.site.register(Measure)

admin.site.register(MeasureGroup)

admin.site.register(WithingsUser)

