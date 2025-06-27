from django.shortcuts import render
from django.http import HttpResponse

def svenska_substantiv(request):
    return render(request, 'svenska_substantiv.html')



