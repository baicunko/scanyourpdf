from celery import Celery, states
from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded
import subprocess
import os
from django.conf import settings
import secrets
import datetime
from .models import ProcessingTask, ProcessedFile
from PyPDF2 import PdfFileReader, utils

# Initialize Celery
celery_app = Celery('pdfwebsite')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')

@shared_task(bind=True, soft_time_limit=30, time_limit=35)
def process_pdf_task(self, file_path, color, task_id):
    try:
        # Update task status
        task = ProcessingTask.objects.get(id=task_id)
        task.status = 'PROCESSING'
        task.save()

        # Validate PDF
        if not is_pdf_valid(file_path):
            task.status = 'FAILED'
            task.error_message = 'Invalid PDF file or exceeds page limit'
            task.save()
            return None

        # Generate output paths
        now = datetime.datetime.now()
        scan_name = 'Scan_' + str(now.year) + str(now.month) + str(now.day) + '_' + secrets.token_urlsafe(8)
        output_path = os.path.join(settings.MEDIA_ROOT, scan_name + '_.pdf')
        output_path_final = os.path.join(settings.MEDIA_ROOT, scan_name + '.pdf')

        # ImageMagick conversion with improved parameters
        convert_cmd = [
            settings.CONVERT_PATH,
            '-density', '110',
            '-limit', 'memory', '256MiB',  # Memory limit
            '-limit', 'time', '30',  # Time limit in seconds
            file_path,
            '-colorspace', color,
            '-linear-stretch', '3.5%x10%',
            '-blur', '0x0.5',
            '-attenuate', '0.25',
            '+noise', 'Laplacian',
            '-rotate', '0.5',
            output_path
        ]
        
        subprocess.run(convert_cmd, timeout=30, check=True)

        # Ghostscript optimization with improved parameters
        gs_cmd = [
            settings.GHOSTSCRIPT_PATH,
            '-dSAFER',
            '-dBATCH',
            '-dNOPAUSE',
            '-dNOCACHE',
            '-sDEVICE=pdfwrite',
            '-dCompatibilityLevel=1.4',  # Optimize for PDF 1.4
            '-dPDFSETTINGS=/ebook',  # Balanced optimization
            '-dColorImageDownsampleType=/Bicubic',
            '-dGrayImageDownsampleType=/Bicubic',
            '-dMonoImageDownsampleType=/Bicubic',
            '-dColorImageResolution=150',
            '-dGrayImageResolution=150',
            '-dMonoImageResolution=150',
            '-dEmbedAllFonts=true',
            '-dSubsetFonts=true',
            '-dAutoRotatePages=/None',
            '-dOverprint=/simulate',
            '-sOutputFile=' + output_path_final,
            output_path
        ]
        
        subprocess.run(gs_cmd, timeout=30, check=True)

        # Cleanup temporary file
        if os.path.exists(output_path):
            os.remove(output_path)
        
        # Update task status
        task.status = 'COMPLETED'
        task.result_path = scan_name + '.pdf'
        task.save()
        
        return scan_name + '.pdf'

    except SoftTimeLimitExceeded:
        task.status = 'FAILED'
        task.error_message = 'Processing timeout'
        task.save()
        cleanup_files(output_path, output_path_final)
        return None
    except Exception as e:
        task.status = 'FAILED'
        task.error_message = str(e)
        task.save()
        cleanup_files(output_path, output_path_final)
        return None

def cleanup_files(*files):
    for file_path in files:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass

def is_pdf_valid(path):
    try:
        with open(path, 'rb') as file:
            reader = PdfFileReader(file)
            num_pages = reader.getNumPages()
            if num_pages > 10:
                return False
            processed_file = ProcessedFile(pages=num_pages)
            processed_file.save()
            return True
    except (utils.PdfReadError, Exception):
        return False
