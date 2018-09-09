from .models import NutritionDay, NutritionMonth
from datetime import datetime, date, timedelta
import calendar

MONTH_MAP = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
WEEK_MAP = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def get_prev_month(year, month):

    if month == 1:
        return (year-1, 12)
    else:
        return (year, month-1)

def get_next_month(year, month):

    if month == 12:
        return (year+1, 1)
    else:
        return (year, month+1)

def get_day_offset(year, month, day, delta):

    prev_date = date(year, month, day) + timedelta(days=delta)

    if len(NutritionMonth.objects.filter(year=year).filter(month=MONTH_MAP[month-1])) > 0:
        cur_month = NutritionMonth.objects.filter(year=year).get(month=MONTH_MAP[month-1])
    else:
        cur_month = NutritionMonth(year=year, month=MONTH_MAP[month-1], month_num=month, month_slug="%d-%d" % (year, month))
        cur_month.save()

    _slug = "%d-%d-%d" % (year, month, day)
    if len(NutritionDay.objects.filter(day_slug=_slug)) > 0:
        cur_day = NutritionDay.objects.get(day_slug=_slug)
    else:
        cur_day = NutritionDay(month=month, cur_date=date(year, month, day), weekday=WEEK_MAP[prev_date.timetuple().tm_wday], day_slug=_slug)
        cur_day.save()

    return (prev_date.year, prev_date.month, prev_date.day)


def get_month(month, year):

    month_iter = []
    month_cal = calendar.Calendar().itermonthdates(year, month)

    if len(NutritionMonth.objects.filter(year=year).filter(month=MONTH_MAP[month-1])) > 0:
        cur_month = NutritionMonth.objects.filter(year=year).get(month=MONTH_MAP[month-1])
    else:
        cur_month = NutritionMonth(year=year, month=MONTH_MAP[month-1], month_num=month, month_slug="%d-%d" % (year, month))
        cur_month.save()

    count = 0
    week_iter = []
    for day in month_cal:

        _day_t = day.timetuple()
        _slug = "%d-%d-%d" % (_day_t.tm_year, _day_t.tm_mon, _day_t.tm_mday)
        if len(NutritionDay.objects.filter(day_slug=_slug)) > 0:
            cur_day = NutritionDay.objects.get(day_slug=_slug)
        else:
            cur_day = NutritionDay(month=cur_month, cur_date=date(_day_t.tm_year, _day_t.tm_mon, _day_t.tm_mday), weekday=WEEK_MAP[count], day_slug=_slug)
            cur_day.save()
        count+=1
        week_iter.append(cur_day)

        if count%7 == 0:
            count = 0
            month_iter.append(week_iter)
            week_iter = []

    return cur_month, month_iter
