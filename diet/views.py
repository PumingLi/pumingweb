from django.shortcuts import render
from datetime import datetime

def diet(request):
    context = {'current': datetime.now}
    return render(request, 'diet.html', context)
