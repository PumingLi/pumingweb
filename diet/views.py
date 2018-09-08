from django.shortcuts import render

from .models import NutritionDay, NutritionWeek, NutritionMonth

from datetime import datetime, date
import calendar

MONTH_MAP = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
WEEK_MAP = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

def diet(request):

    cal = calendar.Calendar()
    today = datetime.now().timetuple()
    month = cal.itermonthdates(today.tm_year, today.tm_mon)


    if len(NutritionMonth.objects.filter(year=today.tm_year).filter(month=MONTH_MAP[today.tm_mon-1])) > 0:
        cur_month = NutritionMonth.objects.filter(year=today.tm_year).get(month=MONTH_MAP[today.tm_mon-1])
    else:
        cur_month = NutritionMonth(year=today.tm_year, month=MONTH_MAP[today.tm_mon-1])
        cur_month.save()

        count = 0
        w_num = 0
        for day in month:

            if count%7 == 0:
                count = 0
                cur_week = NutritionWeek(month=cur_month, week_num=w_num)
                cur_week.save()
                w_num += 1

            _day_t = day.timetuple()
            cur_day = NutritionDay(week=cur_week, cur_date=date(_day_t.tm_year, _day_t.tm_mon, _day_t.tm_mday), weekday=WEEK_MAP[count])
            cur_day.save()

            count+=1
    context = {'cur_month': MONTH_MAP[today.tm_mon-1], 'cur_year': today.tm_year, 'cur_day': today.tm_mday, 'month': cur_month}

    return render(request, 'diet.html', context)


def day_details(request, day_id):
    context = {'day': NutritionDay.objects.get(id=day_id)}

    return render(request, 'day_details.html', context)
