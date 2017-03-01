from __future__ import unicode_literals

from django.db import models

from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
import logging

# Create your models here.

logger = logging.getLogger(__name__)

UserModel = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


@python_2_unicode_compatible
class HumanAPIUser(models.Model):
    """ A user's HumanAPI credentials, allowing API access """
    user = models.OneToOneField(UserModel, help_text='The user')
    humanId = models.IntegerField(help_text='The HumanAPI user ID')
    access_token = models.TextField(help_text='OAuth access token')
    public_token = models.TextField(
        help_text='OAuth access token secret')
    last_update = models.DateTimeField(
        null=True,
        blank=True,
        help_text="The datetime the user's HumanAPI data was last updated")

    def __str__(self):
        if hasattr(self.user, 'get_username'):
            return self.user.get_username()
        else:  # Django 1.4
            return self.user.username

    def get_user_data(self):
        return {
            'access_token': self.access_token,
            'public_token': self.public_token,
            'user_id': self.humanapi_user_id
        }


"""
https://reference.humanapi.co/#blood-pressure

Property    Type    Description
id          String  The id of the blood pressure reading
userId      String  [deprecated - use humanId]
humanId     String  Unique user identifier
timestamp   Date    The original date and time of the measurement
tzOffset    String  The offset from UTC time in +/-hh:mm (e.g. -04:00)
source      String  The source service for the measurement, where it was created
unit        String  The unit of the measurement value
heartRate   String  The heart rate in BPM captured at the time of measurement
systolic    String  The systolic value captured at the time of measurement
diastolic   String  The diastolic value captured at the time of measurement
createdAt   Date    The time the measurement was created on the Human API server
updatedAt   Date    The time the measurement was updated on the Human API server

"""


@python_2_unicode_compatible
class BloodPressure(models.Model):
    # comment
    id = models.TextField(primary_key=True)  
    userId = models.TextField()
    humanId = models.TextField()
    timestamp = models.DateTimeField()
    tzOffset = models.TextField()
    source = models.TextField()
    unit = models.TextField()
    heartRate = models.TextField()
    systolic = models.TextField()
    diastolic = models.TextField()
    createdAt = models.DateTimeField()
    updatedAt = models.DateTimeField()

    def __str__(self):
        return '%s: %s/%s' % (self.timestamp.date().isoformat() if self.date else None,
                           self.systolic(), self.diastolic())






