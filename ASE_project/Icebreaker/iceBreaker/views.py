from django.http import HttpResponse
from django.shortcuts import render

def message(request):
    return render(request, 'fb3.html')
