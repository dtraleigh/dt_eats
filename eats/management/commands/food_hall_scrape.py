from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
import filecmp, os, smtplib
from email.mime.text import MIMEText

from django.core.management.base import BaseCommand, CommandError
from django.core import mail

def send_email(foodhall):
    addresses = ["leo@dtraleigh.com"]

    for email in addresses:
        with mail.get_connection() as connection:
            subject1 = "Update found at " + foodhall
            body1 = "Check Morgan Street"
            from1 = "eats_test@dtraleigh.com"

            mail.EmailMessage(
                subject1, body1, from1, [email],
                connection=connection,
            ).send()


def transfer_co():
    pass


def morgan_street():
    page_link = "http://www.morganfoodhall.com/dining-tenants/"

    page_response = requests.get(page_link, timeout=10)
    page_content = BeautifulSoup(page_response.content, "html.parser")

    eats = []

    eats_divs = page_content.find_all("h3", {"class": "entry-title"})

    for eat in eats_divs:
        title = eat.find("a").get_text()
        eats.append(title)

    t = datetime.today()
    filename = "morgan_street - " + t.strftime("%m-%d-%y")

    with open(filename, "w", encoding="utf-8") as f:
        for eat in eats:
            f.write("%s\n" % eat)

    y = datetime.today() - timedelta(days=1)
    yesterdays_filename = "morgan_street - " + y.strftime("%m-%d-%y")

    if compare(yesterdays_filename, filename, 'Morgan Street'):
        # remove the file if it's two days old
        dby = datetime.today() - timedelta(days=2)
        dby_filename = "morgan_street - " + dby.strftime("%m-%d-%y")
        try:
            os.remove(dby_filename)
        except FileNotFoundError:
            pass


def compare(f1, f2, foodhall):
    if filecmp.cmp(f1, f2, shallow=True):
        # print("Two files are the same")
        return True
    else:
        # print("two files are NOT the same. Send me an email!")
        send_email(foodhall)
        return False