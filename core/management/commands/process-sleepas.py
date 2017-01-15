# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand  # , CommandError
from core.models import SleepAs
import csv
from datetime import datetime, timedelta
from django.core.files.storage import default_storage


class Command(BaseCommand):
    help = 'Imports SleepAs data from a local SleepAs csv export'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', nargs='+', type=str)

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Running the SleepAs import'))
        for csv_file in options['csv_file']:
            self.stdout.write(self.style.SUCCESS('Processing file: "%s"' % csv_file))
            data = self.read_csv(csv_file)
            # self.stdout.write(self.style.SUCCESS('data : %s' % data))
            self.stdout.write(self.style.SUCCESS('converted file: "%s"' % csv_file))
            self.import_data(data)
            self.stdout.write(self.style.SUCCESS('imported file: "%s"' % csv_file))

    def parse_sleep(self, row, data_events):
        sleep = {}
        # start = datetime.strptime(row[2], '%d/%m/%Y %H:%M:%S')
        # end = datetime.strptime(row[3], '%d/%m/%Y %H:%M:%S')
        start = datetime.strptime(row[2], '%d. %m. %Y %H:%M')
        end = datetime.strptime(row[3], '%d. %m. %Y %H:%M')
        date = start.date()

        sleep['id'] = int(row[0])
        sleep['Tz'] = row[1]
        if start.hour < 12:
            date = date - timedelta(1)
        sleep['date'] = date.isoformat()
        sleep['weekday'] = date.isoweekday()  # Mon: 1 - Sun: 7
        sleep['start_time'] = start.strftime('%Y-%m-%d %H:%M')
        sleep['end_time'] = end.strftime('%Y-%m-%d %H:%M')
        sleep['length'] = (end - start).total_seconds() / 3600
        sleep['cycles'] = int(row[11])
        sleep['deep'] = float(row[12])
        sleep['Geo'] = int(row[13])
        for i in range(0, 24):
            if i > 9:
                hour = str(i)
            else:
                hour = "0" + str(i)
            for j in ['00', '06', '12', '18', '24', '30', '36', '42', '48', '54']:
                time = hour + ':' + j
                if time in data_events:
                    value = data_events[time]
                else:
                    value = -1
                sleep[time] = value
        return sleep

    def filter_times(self, keys, values):
        if len(keys) != len(values):
            raise Exception("Length of keys must match length of values")
        filtered_columns = []
        time_columns = []
        for i in range(len(keys)):
            if keys[i] == 'Event':
                filtered_columns.append(values[i])
            else:
                time_columns.append([keys[i], values[i]])
        events = {}
        times = {}
        for time in time_columns:
            if len(time[0]) < 1:
                continue
            value = time[1]
            t = time[0].split(':')
            lower_time_bound = int(int(t[1]) / 6) * 6
            # upper_time_bound = lower_time_bound + 6
            if lower_time_bound < 10:
                t = str(t[0]) + ':0' + str(lower_time_bound)
            else:
                t = str(t[0]) + ':' + str(lower_time_bound)
            if t not in times:
                times[t] = []
            times[t] = value
        for event in filtered_columns:
            e = event.split('-')
            if e[0] not in events:
                events[e[0]] = []
            events[e[0]].append(datetime.fromtimestamp(int(e[1]) / 1000))
        return times

    def read_csv(self, filename):
        # TODO: make permanent (maybe a selector from Dropbox for the SleepAsConfig filename)

        if default_storage.exists('/Apps/Sleep Cloud Backup/Sleep as Android Data'):
            with default_storage.open('/Apps/Sleep Cloud Backup/Sleep as Android Data', 'r') as csvfile:
                source = csv.reader(csvfile)
                header = False
                data_sleep = []
                event_key = None
                for row in source:
                    if len(row[0]) < 1:
                        continue
                    header = not header
                    if header:
                        event_key = tuple(row[15:])
                    else:
                        event_value = tuple(row[15:])
                        data_events = self.filter_times(event_key, event_value)
                        row = self.parse_sleep(row, data_events)
                        if not len(row) < 1:
                            data_sleep.append(row)
                return data_sleep
        else:
            self.style.FAILURE("file doesn't exist")
            exit

    def import_data(self, data):
        num_epochs = 5

        for row in data:
            # self.stdout.write(self.style.SUCCESS('row: "%s"' % row))
            # self.stdout.write(self.style.SUCCESS('row id: "%s"' % row['id']))
            sleep = SleepAs()
            sleep._id = int(row['id'])
            sleep.Tz = row['Tz']
            sleep.date = row['date']
            sleep.weekday = row['weekday']
            sleep.start_time = row['start_time']
            sleep.end_time = row['end_time']
            sleep.length = row['length']
            sleep.cycles = int(row['cycles'])
            sleep.deep = float(row['deep'])
            sleep.Geo = int(row['Geo'])
            sleep.awake_during_the_night = 0
            sleep.sleep_data = "not used yet"

            start_date = datetime.strptime(row['start_time'], '%Y-%m-%d %H:%M')
            starttime = start_date.time()
            # end_date = datetime.strptime(row['end_time'], '%Y-%m-%d %H:%M')
            # endtime = end_date.time()

            # do 8pm to midnight
            for i in range(20, 23):
                hour = i
                for j in range(0, 9):
                    # set the minute
                    minute = j * 6
                    # get the next num_epochs values
                    value = 0
                    for k in range(0, num_epochs):
                        minute = (j + k) * 6
                        if minute > 59:
                            minute = minute - 60
                            if hour == 23:
                                hour = "00"
                            else:
                                hour = int(hour) + 1
                        if minute < 10:
                            minute = "0" + str(minute)
                        if hour < 10:
                            hour = "0" + str(hour)
                        time = str(hour) + ":" + str(minute)

                        value = value + float(row[time])
                    # reset hour and minute
                    hour = i
                    minute = j * 6
                    if minute < 10:
                        minute = "0" + str(minute)
                    if hour < 10:
                        hour = "0" + str(hour)
                    # set the awake... value (if asleep)
                    curr_time = (datetime.strptime(time, '%H:%M')).time()
                    if curr_time > starttime:
                        if value > 15:
                            sleep.awake_during_the_night = sleep.awake_during_the_night + 1

            # do midnight to 8pm...
            for i in range(0, 20):
                hour = i
                for j in range(0, 9):
                    # set the minute
                    minute = j * 6
                    # get the next num_epochs values
                    value = 0
                    for k in range(0, num_epochs):
                        minute = (j + k) * 6
                        if minute > 59:
                            minute = minute - 60
                            if hour == 23:
                                hour = "00"
                            else:
                                hour = int(hour) + 1
                        if minute < 10:
                            minute = "0" + str(minute)
                        if hour < 10:
                            hour = "0" + str(hour)
                        time = str(hour) + ":" + str(minute)
                        value = value + float(row[time])
                    # reset hour and minute
                    hour = i
                    minute = j * 6
                    if minute < 10:
                        minute = "0" + str(minute)
                    if hour < 10:
                        hour = "0" + str(hour)
                    # set the awake... value (if asleep)
                    curr_time = (datetime.strptime(time, '%H:%M')).time()
                    if curr_time > starttime:
                        if value > 15:
                            sleep.awake_during_the_night = sleep.awake_during_the_night + 1
            sleep.save()
        return 1

