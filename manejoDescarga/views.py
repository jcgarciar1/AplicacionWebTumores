from django.http import HttpResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg
from django.shortcuts import render, redirect
from manejoDescarga.redes import predict_final
import numpy as np
import cv2
import os
# Create your views here.

from django.core.files.storage import FileSystemStorage

filename = ""
def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        global filename
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'simple_upload.html')

def get_filename():
    return filename

def plot(request):
    imagen = '/Users/juancgarcia/Downloads/PaginaTesis/media/' + filename
    imagen = cv2.imread(imagen)
    fig = predict_final(imagen)
    fig.savefig('/Users/juancgarcia/Downloads/PaginaTesis/PaginaTesis/static/images/nueva.png')
    #response = HttpResponse(content_type='image/png')
    #canvas = FigureCanvasAgg(fig)
    #canvas.print_png(response)
    return render(request, 'index.html')