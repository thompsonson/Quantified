# -*- coding: utf-8 -*-
from withingsapp.models import *
from withingsapp import utils
from django.contrib.auth.models import User
import logging

logger = logging.getLogger('tasks'')


def update_measurements():
    logger.info("Running WiThings update_measurements")
    # hard coded user_id (for the time being/individual use)
    # TODO: loop through all users, that are previously authenticated with WiThings
    user_id = 1
    user = User.objects.get(id=user_id)

    # get the withings user
    withings_user = WithingsUser.objects.filter(user_id=user_id).first()
    #withings_user = withings_user[0]

    logger.info("processing for user: %s" % withings_user)

    # call the withings API service
    api = utils.create_withings(**withings_user.get_user_data())

    logger.info("Authenticated and requesting measures")

    measure_groups_created, measures_created = MeasureGroup.create_from_measures(user, api.get_measures())

    logger.info("Complete")
