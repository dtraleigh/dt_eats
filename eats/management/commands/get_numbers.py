from django.core.management.base import BaseCommand, CommandError
from eats.models import Business

class Command(BaseCommand):

    def handle(self, *args, **options):
        the_locals = Business.objects.filter(not_local=False, display_on_site=True)
        not_the_locals = Business.objects.filter(not_local=True, display_on_site=True)

        self.stdout.write('Local count: ' + str(the_locals.count()) + '\n')
        self.stdout.write('Non-local count: ' + str(not_the_locals.count()) + '\n')
