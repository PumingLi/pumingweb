from django.shortcuts import render
from datetime import datetime
import calendar

MONTH_MAP = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
WEEK_MAP = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def diet(request):

    cal = calendar.Calendar()
    today = datetime.now().timetuple()

    month = cal.itermonthdays4(today.tm_year, today.tm_mon)

    month_matrix = []
    _week = []
    count = 0
    for day in month:

        _day = list(day)
        _day[1] = MONTH_MAP[day[1]]
        _day[3] = WEEK_MAP[day[3]]
        _week.append(_day)
        count += 1
        if count % 7 == 0 and count != 0:
            month_matrix.append(_week)
            _week = []
            count = 0



    context = {'cur_month': MONTH_MAP[today.tm_mon], 'cur_year': today.tm_year, 'cur_day': today.tm_mday, 'month_matrix': month_matrix, "week_map": WEEK_MAP, "month_map": MONTH_MAP}

    return render(request, 'diet.html', context)
