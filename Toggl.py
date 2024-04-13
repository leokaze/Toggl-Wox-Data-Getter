import requests
from base64 import b64encode
import json

import datetime
from pytz import timezone
import pytz


class Toggl():
    def __init__(self):
        self.start_date = None
        self.end_date = None
        self.yesterday = None
        self.toggl_url = "https://api.track.toggl.com/api/v9/me/time_entries?"
        self.from_date = ""
        self.to_date = ""
        self.credentials = b'YOUR_EMAIL:YOUR_PASSWORD'
        self.time_zone = 'America/La_Paz'

    def GET_YESTERDAY_DATA(self):
        today = datetime.date.today()
        start_date = today - datetime.timedelta(days=2)
        self.start_date = start_date.strftime("%Y-%m-%d")
        yesterday = today - datetime.timedelta(days=1)
        self.yesterday = yesterday.strftime("%Y-%m-%d")
        tomorrow = today + datetime.timedelta(days=1)
        self.end_date = tomorrow.strftime("%Y-%m-%d")
        entries = self.get_toggl_data()
        entries = self.change_times_of_entries(entries)

        filtered_data = {}

        for entry in entries:
            start = entry['start']
            if self.yesterday in start:
                key = entry['project_name'] + ' - ' + entry['description']
                if key in filtered_data:
                    filtered_data[key] += entry['duration']
                else:
                    filtered_data[key] = entry['duration']

        data = self.get_formated_data(filtered_data)
        # data = json.dumps(data, indent=4)
        data = self.get_printable_data(data)
        return data
    
    def GET_LAST_WEEK_DATA(self):
        # the week start in monday and ends in sunday
        today = datetime.date.today()
        start_date = today - datetime.timedelta(days=7)
        start_date = start_date - datetime.timedelta(days=start_date.weekday())
        self.start_date = start_date.strftime("%Y-%m-%d")
        end_date = today - datetime.timedelta(days=today.weekday())
        self.end_date = end_date.strftime("%Y-%m-%d")

        last_sunday = today - datetime.timedelta(days=today.weekday()+1)

        entries = self.get_toggl_data()
        entries = self.change_times_of_entries(entries)

        self.end_date = last_sunday.strftime("%Y-%m-%d")

        self.from_date = self.start_date
        self.to_date = self.end_date

        filtered_data = {}
        project_name_data = {}

        for entry in entries:
            start = entry['start']
            if self.get_if_date_is_in_range(start):
                key = entry['project_name'] + ' - ' + entry['description']
                if key in filtered_data:
                    filtered_data[key] += entry['duration']
                else:
                    filtered_data[key] = entry['duration']

                key = entry['project_name']
                if key in project_name_data:
                    project_name_data[key] += entry['duration']
                else:
                    project_name_data[key] = entry['duration']

        
        data = self.get_formated_data(filtered_data)
        project_data = self.get_formated_data(project_name_data)
        # data = json.dumps(data, indent=4)
        data = self.get_printable_data(data, project_data)
        return data
    
    def GET_LAST_MONTH_DATA(self):
        # get the last month data
        year = datetime.date.today().year
        month = datetime.date.today().month - 1

        if month == 0:
            month = 12
            year -= 1

        first_day_of_month = datetime.date(year, month, 1)
        last_day_of_month = datetime.date(year, month + 1, 1) - datetime.timedelta(days=1)

        self.start_date = first_day_of_month.strftime("%Y-%m-%d")
        self.end_date = last_day_of_month.strftime("%Y-%m-%d")

        self.from_date = self.start_date
        self.to_date = self.end_date

        entries = self.get_toggl_data()
        entries = self.change_times_of_entries(entries)

        filtered_data = {}
        project_name_data = {}

        for entry in entries:
            start = entry['start']
            if self.get_if_date_is_in_range(start):
                key = entry['project_name'] + ' - ' + entry['description']
                if key in filtered_data:
                    filtered_data[key] += entry['duration']
                else:
                    filtered_data[key] = entry['duration']

                key = entry['project_name']
                if key in project_name_data:
                    project_name_data[key] += entry['duration']
                else:
                    project_name_data[key] = entry['duration']


        data = self.get_formated_data(filtered_data)
        project_data = self.get_formated_data(project_name_data)

        data = self.get_printable_data(data, project_data)
        return data
    
    def get_if_date_is_in_range(self, date):
        # convert string date to datetime
        date = date[:10]
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
        start_date = datetime.datetime.strptime(self.start_date, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(self.end_date, '%Y-%m-%d')
        return start_date <= date <= end_date
    
    def seconds_to_hours_string(self, seconds):
        return str(seconds // 3600) + ':' + str((seconds % 3600) // 60) + ':' + str(seconds % 60)
    
    def get_formated_data(self, data):
        labels = []
        series_hours = []
        series_seconds = []
        series_time_format = []
        total_seconds = 0
        total_hours_string = ''
        for key in data:
            labels.append(key)
            series_hours.append(self.roundToFiveDecimals(data[key] / 3600))
            series_seconds.append(data[key])
            series_time_format.append(self.seconds_to_hours_string(data[key]))
            total_seconds += data[key]

        total_hours_string = self.seconds_to_hours_string(total_seconds)

        # sort all by series in decreasing order
        labels, series_hours, series_seconds, series_time_format = zip(*sorted(zip(labels, series_hours, series_seconds, series_time_format), key=lambda x: x[1], reverse=True))

        formated_data = {
            'labels': list(labels),
            'series_hours': list(series_hours),
            'series_seconds': list(series_seconds),
            'series_time_format': list(series_time_format),
            'total_hours_string': total_hours_string,
            'total_seconds': total_seconds
        }

        return formated_data

    
    def get_toggl_data(self):
        toggl_request_string = self.toggl_url + "start_date=" + self.start_date + "&end_date=" + self.end_date + "&meta=true"
        headers = {
            'content-type': 'application/json',
            'Authorization' : 'Basic %s' %  b64encode(self.credentials).decode("ascii")
        }
        entries_data_json = requests.get(toggl_request_string, headers=headers)
        entries = entries_data_json.json()
        return entries
    
    def change_times_of_entries(self, entries):
        for entry in entries:
            entry['start'] = self.convert_utc_to_local(entry['start'])
            entry['stop'] = self.convert_utc_to_local(entry['stop'])
        return entries
    
    # convert UTC time to local Bolivia time
    def convert_utc_to_local(self, utc_dt):
        if(utc_dt == None):
            return 'NONE'
        utc_dt = datetime.datetime.strptime(utc_dt, '%Y-%m-%dT%H:%M:%S+00:00')
        local_tz = timezone(self.time_zone)
        local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
        return local_dt.strftime('%Y-%m-%d %H:%M:%S')
    
    def roundToFiveDecimals(self, number):
        return round(number, 5)
    
    def ENG_date_to_ES(self, date = "Sunday 07 de April de 2024"):
        months = {
            "January": "Enero",
            "February": "Febrero",
            "March": "Marzo",
            "April": "Abril",
            "May": "Mayo",
            "June": "Junio",
            "July": "Julio",
            "August": "Agosto",
            "September": "Septiembre",
            "October": "Octubre",
            "November": "Noviembre",
            "December": "Diciembre"
        }

        days = {
            "Monday": "Lunes",
            "Tuesday": "Martes",
            "Wednesday": "Miércoles",
            "Thursday": "Jueves",
            "Friday": "Viernes",
            "Saturday": "Sábado",
            "Sunday": "Domingo"
        }

        date = date.split(" ")
        date[0] = days[date[0]]
        date[3] = months[date[3]]
        return " ".join(date)
    
    def get_printable_data(self, data, project_data = None):
        # DATA START
        # ```chart
        # type: doughnut
        # labels: ['Farmacorp Drones - Animación', 'oscio - game', 'oscio - otros']
        # series:
        #   - title: Tiempos
        #     data: [9.20528, 3.79722, 2.4775]
        # width: 50%
        # labelColors: true
        # ```

        # > [!summary] 
        # > TOTAL: 5:00:00
        # > rest of labels
        # DATA END

        chart_data = '```chart\n'
        chart_data += 'type: doughnut\n'
        chart_data += 'labels: ' + str(data['labels']) + '\n'
        chart_data += 'series:\n'
        chart_data += '  - title: Tiempos\n'
        chart_data += '    data: ' + str(data['series_hours']) + '\n'
        chart_data += 'width: 50%\n'
        chart_data += 'labelColors: true\n'
        chart_data += '```\n\n'

        summary_data = '> [!summary]\n'

        if(self.from_date != ''):
            from_date = datetime.datetime.strptime(self.from_date, '%Y-%m-%d')
            from_date = from_date.strftime('%A %d de %B de %Y')
            from_date = self.ENG_date_to_ES(from_date)
            summary_data += '> DESDE: ' + from_date + '\n'
            to_date = datetime.datetime.strptime(self.to_date, '%Y-%m-%d')
            to_date = to_date.strftime('%A %d de %B de %Y')
            to_date = self.ENG_date_to_ES(to_date)
            summary_data += '> HASTA: ' + to_date + '\n'
            summary_data += '>\n'
        else:
            yesterday = datetime.datetime.strptime(self.yesterday, '%Y-%m-%d')
            yesterday = yesterday.strftime('%A %d de %B de %Y')
            yesterday = self.ENG_date_to_ES(yesterday)
            summary_data += '> FECHA: ' + yesterday + '\n'
            summary_data += '>\n'

        summary_data += '> TOTAL: ' + data['total_hours_string'] + '\n'
        for i in range(len(data['labels'])):
            summary_data += '> ' + data['labels'][i] + ': ' + data['series_time_format'][i] + '\n'

        if(project_data != None):
            summary_data += '> \n'
            summary_data += '> PROJECTS TOTALS\n'
            for i in range(len(project_data['labels'])):
                summary_data += '> ' + project_data['labels'][i] + ': ' + project_data['series_time_format'][i] + '\n'

        return chart_data + summary_data

