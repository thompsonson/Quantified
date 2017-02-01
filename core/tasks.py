# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger('tasks')

logger.info("loading modules")

from django.core.models import aTimeLogger
from django.core.files.storage import default_storage
from datetime import datetime
import csv


def import_aTimeLogger_csv(filename='/Quantified/report.csv'):
    # TODO: make permanent (maybe a selector from Dropbox for the FileConfig file_type 'SleepAs')
    activities_created = 0
    logger.info("check for report.csv from Dropbox folder: %s" % filename)
    exit

    if default_storage.exists(filename):
        logger.info("reading report.csv from Dropbox folder")
        with default_storage.open(filename, 'r') as csvfile:
            source = csv.reader(csvfile)
            for row in source:
                if len(row) < 1:
                    break
                if row[0] == "Activity type":
                    continue  # skip the header
                logger.debug('row: "%s"' % row)
                aTL, created = aTimeLogger.objects.get_or_create(
                    ActivityType=row[0],
                    Duration=row[1],
                    start_time=datetime.strptime(row[2], '%Y-%m-%d %H:%M'),
                    end_time=datetime.strptime(row[3], '%Y-%m-%d %H:%M'),
                    Comment=row[4]
                )
                created = 0
                if created:
                    activities_created = activities_created + 1
            logger.info('completed, %d activites created' % activities_created)
            return activities_created
    else:
        logger.info("aTimeLogger report csv doesn't exist")
        return -1
