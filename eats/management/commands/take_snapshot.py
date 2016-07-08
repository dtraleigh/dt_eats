#////
#This management command creates a snapshot object which is used to track
#the number of local and not local businesses in the database at a given point in time.
#This command is run by cron.
#\\\\

from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from eats.models import Business, snapshot
import datetime

class Command(BaseCommand):

    def handle(self, *args, **options):
        the_locals = Business.objects.filter(
                    Q(open_date__lte=datetime.datetime.today()) &
                    (Q(close_date=None) | Q(close_date__gt=datetime.datetime.today()))).filter(not_local=False)
        not_the_locals = Business.objects.filter(
                    Q(open_date__lte=datetime.datetime.today()) &
                    (Q(close_date=None) | Q(close_date__gt=datetime.datetime.today()))).filter(not_local=True)
        all_active_businesses = Business.objects.filter(
                    Q(open_date__lte=datetime.datetime.today()) &
                    (Q(close_date=None) | Q(close_date__gt=datetime.datetime.today())))

        new_snapshot = snapshot(local_business_count=the_locals.count(),
                            not_local_business_count=not_the_locals.count())
        new_snapshot.save()

        for active_business in all_active_businesses:
            new_snapshot.businesses.add(active_business.id)
