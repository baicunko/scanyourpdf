import datetime
import os
import secrets
import subprocess
import urllib.parse

from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db.models import Sum

from .models import File, ProcessedFile, ProcessingTask
from .tasks import process_pdf_task


#Source: https://tex.stackexchange.com/questions/94523/simulate-a-scanned-paper
#Source 2:http://www.imagemagick.org/discourse-server/viewtopic.php?t=33085
#I adapted the method a little bit with what I thought would work better
#Output PDF from ImageMagick is way bigger due to rasterization. GhostScript used afterwards for bringing size back down
#If someone has any ideas how to optimize it further, please feel free.
#Author: Cristian Lehuede request.POST['exampleRadios']

def upload(request):
    if request.method == 'POST':
        try:
            uploaded_file = request.FILES['document']
            if uploaded_file.size > 52428000:  # 50MB limit
                return JsonResponse({
                    'status': 'error',
                    'message': 'PDF is larger than 50MB'
                })

            color = 'gray' if request.POST.get('exampleRadios', 'gray') == 'gray' else 'sRGB'
            
            # Save the uploaded file
            fs = FileSystemStorage()
            name = fs.save(uploaded_file.name, uploaded_file)
            file_path = os.path.join(settings.MEDIA_ROOT, name)

            # Create processing task
            task = ProcessingTask.objects.create()
            
            # Launch async processing
            process_pdf_task.delay(file_path, color, task.id)
            
            return JsonResponse({
                'status': 'success',
                'task_id': task.id
            })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })

    context = {
        'processed_pages': ProcessedFile.objects.aggregate(Sum('pages'))['pages__sum']
    }
    return render(request, 'pdfwebsite/upload.html', context)

def check_status(request, task_id):
    try:
        task = ProcessingTask.objects.get(id=task_id)
        response = {
            'status': task.status,
            'created_at': task.created_at.isoformat()
        }
        
        if task.status == 'COMPLETED':
            response['url'] = f'/media/{task.result_path}'
        elif task.status == 'FAILED':
            response['error'] = task.error_message
            
        return JsonResponse(response)
    except ProcessingTask.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Task not found'}, status=404)