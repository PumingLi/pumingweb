from django.shortcuts import render
from datetime import datetime
import calendar

MONTH_MAP = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
WEEK_MAP = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def diet(request):

    cal = calendar.Calendar()
    today = datetime.now().timetuple()
    month = cal.itermonthdates(today.tm_year, today.tm_mon)

    month_matrix = []
    _week = []
    count = 0
    for day in month:
        _day_t = day.timetuple()
        _week.append((_day_t.tm_year, MONTH_MAP[_day_t.tm_mon], _day_t.tm_mday, WEEK_MAP[count]))
        count += 1
        if count % 7 == 0 and count != 0:
            month_matrix.append(_week)
            _week = []
            count = 0

    context = {'cur_month': MONTH_MAP[today.tm_mon], 'cur_year': today.tm_year, 'cur_day': today.tm_mday, 'month_matrix': month_matrix, "week_map": WEEK_MAP, "month_map": MONTH_MAP}
    return render(request, 'diet.html', context)


def results(request, question_id):

    return render(request, 'results.html', {'question': question})
