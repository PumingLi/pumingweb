from django.shortcuts import render
from django.http import HttpResponse
import calendar

def home(request):

    cal = calendar.Calendar()
    # today = datetime.now().timetuple()

    month = cal.itermonthdates(2018, 8)


    return render(request, 'home.html', {'month': month})
