from django.core.management.base import BaseCommand
import stanza


class Command(BaseCommand):
    help = 'Populates the database with the supported brands'

    def handle(self, *args, **options):
        
        stanza.download('es')