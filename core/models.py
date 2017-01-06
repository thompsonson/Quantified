from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.


@python_2_unicode_compatible
class SleepAs(models.Model):
    _id = models.BigIntegerField()
    Tz = models.CharField(max_length=50)
    date = models.DateField()
    weekday = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    length = models.DecimalField(decimal_places=10, max_digits=13)
    cycles = models.IntegerField()
    deep = models.DecimalField(decimal_places=10, max_digits=13)
    Geo = models.TextField()
    awake_during_the_night = models.IntegerField()
    sleep_data = models.TextField()

    def __str__(self):
        return str(self._id)
        # return "test"

#    def __unicode__(self):
#        return str(self._id)

