from django.core.management.base import BaseCommand, CommandError
from django.core import mail

from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
import filecmp, os, smtplib
from email.mime.text import MIMEText

from .food_hall_scrape import *

class Command(BaseCommand):

    def handle(self, *args, **options):
        morgan_street()
        transfer_co()