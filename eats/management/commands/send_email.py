from django.core.management.base import BaseCommand, CommandError
from django.core import mail

import datetime

class Command(BaseCommand):

    def handle(self, *args, **options):
        addresses = ["leo@dtraleigh.com"]

        for email in addresses:
            with mail.get_connection() as connection:
                subject1 = "Test from Djangobox"
                body1 = "This should be the body of the email."
                from1 = "eats_test@dtraleigh.com"

                mail.EmailMessage(
                    subject1, body1, from1, [email],
                    connection=connection,
                ).send()