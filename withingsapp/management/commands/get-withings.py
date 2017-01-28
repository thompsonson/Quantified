# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand  # , CommandError
from withingsapp.models import *
from withingsapp import utils
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Imports WiThings data for a pre-authenticated user'

    def add_arguments(self, parser):
        parser.add_argument('user_id', nargs='+', type=str)

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Running the WiThings import'))

        # hard coded user_id (for the time being/individual use)
        # TODO: loop through all users, that are previously authenticated with WiThings
        user_id = 1
        user = User.objects.get(id=user_id)

        # get the withings user
        withings_user = WithingsUser.objects.filter(user_id=user_id).first()
        #withings_user = withings_user[0]

        # call the withings API service
        api = utils.create_withings(**withings_user.get_user_data())

        MeasureGroup.create_from_measures(user, api.get_measures())

        self.stdout.write(self.style.SUCCESS('Finnished WiThings import'))



