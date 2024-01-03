from django.core.management.base import BaseCommand
from smiteinfo.models import God


class Command(BaseCommand):
    help = "Triggers updates for dynamic fields in all God instances"

    def handle(self, *args, **options):
        for god in God.objects.all():
            god.save()
