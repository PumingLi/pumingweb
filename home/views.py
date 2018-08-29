from django.shortcuts import render
from django.http import HttpResponse
import calender

def home(request):

    cal = calendar.Calendar()
    today = datetime.now().timetuple()

    month = cal.itermonthdates(today.tm_year, today.tm_mon)


    return render(request, 'home.html')
