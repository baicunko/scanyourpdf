from django.db import models

class File(models.Model):
	path=models.CharField(max_length=255)
	date_posted=models.DateTimeField(auto_now_add=True)

class ProcessedFile(models.Model):
	pages=models.IntegerField()
	date_scanned=models.DateTimeField(auto_now_add=True)

	
class ProcessingTask(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]
    
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    result_path = models.CharField(max_length=255, null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)