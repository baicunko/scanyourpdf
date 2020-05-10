from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from urllib.parse import urlparse
import os
from pdfwebsite.models import File
from datetime import datetime, timedelta

#File will check DB and delete files older than 1 hour.

class Command(BaseCommand):
    help = 'Cleans old files'

    def handle(self, *args, **kwargs):
        time_threshold = datetime.now() - timedelta(hours=1)
        results = File.objects.filter(date_posted__lt=time_threshold)
        for file in results:
        	path=file.path
        	try:
        		os.remove(path)
        	except OSError:
        		pass
        	file.delete()
