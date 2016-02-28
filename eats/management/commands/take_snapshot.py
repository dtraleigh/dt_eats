from django.core.management.base import BaseCommand, CommandError
from eats.models import Business, snapshot

class Command(BaseCommand):

    def handle(self, *args, **options):
        the_locals = Business.objects.filter(not_local=False, display_on_site=True)
        not_the_locals = Business.objects.filter(not_local=True, display_on_site=True)
        all_active_businesses = Business.objects.filter(display_on_site=True)

        new_snapshot = snapshot(local_business_count=the_locals.count(),
                            not_local_business_count=not_the_locals.count())
        new_snapshot.save()

        for active_business in all_active_businesses:
            new_snapshot.businesses.add(active_business.id)
