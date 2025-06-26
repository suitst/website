from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return(HttpResponse("Hello world, you are at the home page."))