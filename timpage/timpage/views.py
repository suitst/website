from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'home.html')

def cv(request):
    return render(request, 'cv.html')

def gallery(request):
    return render(request, 'gallery.html')