from django.db import models

class File(models.Model):
	path=models.CharField(max_length=255)
	date_posted=models.DateTimeField(auto_now_add=True)
