from django.core.management.base import BaseCommand, CommandError
from django.core import mail
from django.core.mail import send_mail


class Command(BaseCommand):

    def handle(self, *args, **options):
        addresses = ["leo@dtraleigh.com"]
        #
        # for email in addresses:
        #     with mail.get_connection() as connection:
        #         subject1 = "Test from Djangobox"
        #         body1 = "This should be the body of the email."
        #         from1 = "eats_test@dtraleigh.com"
        #         html_message = None
        #
        #         mail.EmailMessage(
        #             subject1, body1, from1, [email],
        #             connection=connection,
        #         ).send()

        subject1 = "Test from Djangobox"
        body1 = "This should be the body of the email with a link to DTRaleigh: https://dtraleigh.com"
        from1 = "eats_test@dtraleigh.com"
        #html_message = "This should be the body of the email with a <a href=\"https://dtraleigh.com\">link</a>"
        fail_silently = None

        send_mail(
            subject1,
            body1,
            from1,
            addresses,
            #html_message,
            fail_silently
        )

