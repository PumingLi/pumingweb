from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from time import gmtime, strftime

def about(request):
    return render(request, 'about.html')
