from django.shortcuts import render
from django.http import HttpResponse

from graphos.sources.simple import SimpleDataSource
from graphos.renderers.gchart import LineChart

def home(request):

    return render(request, 'home.html')
