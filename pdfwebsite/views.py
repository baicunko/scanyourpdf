import datetime
import os
import secrets
import subprocess
import urllib.parse

from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from PyPDF2 import PdfFileWriter, PdfFileReader, utils

from pdfwebsite.models import File


def home(request):
	return render(request, 'pdfwebsite/home.html')


#Source: https://tex.stackexchange.com/questions/94523/simulate-a-scanned-paper
#Source 2:http://www.imagemagick.org/discourse-server/viewtopic.php?t=33085
#I adapted the method a little bit with what I thought would work better
#Output PDF from ImageMagick is way bigger due to rasterization. GhostScript used afterwards for bringing size back down
#If someone has any ideas how to optimize it further, please feel free.
#Author: Cristian Lehuede

def upload(request):
	response={}
	if request.method == 'POST':
		uploaded_file = request.FILES['document']
		response=processPDF(uploaded_file)

	return render(request, 'pdfwebsite/upload.html', response)


def processPDF(uploaded_file):
	context = {}
	fs = FileSystemStorage()
	if uploaded_file.size>104857600:
		context['error']='PDF is larger than 100MB, please recheck uploaded file'
		return context

	name = fs.save(uploaded_file.name,uploaded_file)
	dirspot = os.getcwd()
	dirspot=dirspot+fs.url(name)
	now = datetime.datetime.now()

	# 8 bytes of randomness on the end of the path should be sufficient -
	# it is more than can be brute-forced in any reasonable amount of time
	# over the network, especially with the cleanup task removing files every
	# hour.
	scan_name='Scan_' + str(now.year) + str(now.month) + str(now.day) + '_' + secrets.token_urlsafe(8)
	dirspot=urllib.parse.unquote(dirspot)
	validate_file=isPdfValid(dirspot)
	if validate_file:
		output_path=os.getcwd()+'/media/'+scan_name+'_.pdf'
		output_path_final=os.getcwd()+'/media/'+scan_name+'.pdf'
		cmd = ['/usr/local/bin/convert','-density','150',dirspot,'-colorspace','gray','-linear-stretch','3.5%x10%','-blur','0x0.5','-attenuate','0.25','+noise','Gaussian','-rotate','0.5',output_path]
		print (cmd)
		subprocess.call(cmd, shell=False)
		cmd_gs = ['/usr/local/bin/gs','-dSAFER','-dBATCH','-dNOPAUSE','-dNOCACHE','-sDEVICE=pdfwrite','-sColorConversionStrategy=LeaveColorUnchanged','-dAutoFilterColorImages=true','-dAutoFilterGrayImages=true','-dDownsampleMonoImages=true','-dDownsampleGrayImages=true','-dDownsampleColorImages=true','-sOutputFile='+output_path_final, output_path]
		subprocess.call(cmd_gs, shell=False)
		context['url'] = '/media/'+scan_name+'.pdf'
		file_save_to_db=File(path=output_path_final)
		file_save_to_db.save()
	else:
		context['error']='PDF is not valid, please recheck uploaded file'

	os.remove(output_path)
	os.remove(dirspot)
	return context



def isPdfValid(path):
	try:
		reader=PdfFileReader(open(path,'rb'))
		num_pages = reader.getNumPages()
		if num_pages>100:
			return True

		return True
	except utils.PdfReadError:
		print("invalid PDF file")
		return False
	else:
		return True
