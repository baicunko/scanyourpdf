import os
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from pdfwebsite.models import File


class Command(BaseCommand):
    help = 'Removes files that are more than an hour old'

    def handle(self, *args, **kwargs):
        time_threshold = timezone.now() - timedelta(hours=1)
        results = File.objects.filter(date_posted__lt=time_threshold)
        for file in results:
            path = file.path
            try:
                os.remove(path)
            except OSError:
                pass
            file.delete()
