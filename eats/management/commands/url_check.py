import requests

from django.core.management.base import BaseCommand, CommandError
from django.core import mail
from eats.models import *
from django.db.models import Q

class Command(BaseCommand):

    def handle(self, *args, **options):
        all_open_places = Business.objects.filter(~Q(close_date__lt=datetime.datetime.today())).order_by('name')

        places_with_problems = []
        places_with_400s = []
        places_with_300s = []
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/56.0.2924.76 Safari/537.36'
        }

        for place in all_open_places:
            try:
                status_code = requests.head(place.link, timeout=5, headers=headers).status_code
                # if 299 < status_code < 399:
                if status_code > 299 and status_code < 399:
                    places_with_300s.append(place)
                # elif 399 < status_code < 499:
                if status_code > 399 and status_code < 499:
                    places_with_400s.append(place)

            except:
                places_with_problems.append(place)

        message = "Problem sites:\n"
        message += self.list_sites(places_with_problems)
        message += "400 Sites:\n"
        message += self.list_sites(places_with_400s)
        message += "300 Sites:\n"
        message += self.list_sites(places_with_300s)

        self.send_message_email(message)

    def list_sites(self, places):
        message = ""
        if places:
            for place in places:
                message += place.name + "\n"

            return message
        return "\n"

    def send_message_email(self, message):
        addresses = ["leo@dtraleigh.com"]

        for email in addresses:
            with mail.get_connection() as connection:
                subject1 = "Message from Eats URL Check."
                body1 = message
                from1 = "eats_test@dtraleigh.com"

                mail.EmailMessage(
                    subject1, body1, from1, [email],
                    connection=connection,
                ).send()

