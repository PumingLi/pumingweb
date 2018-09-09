from django.shortcuts import render

from .models import NutritionDay, NutritionMonth
from .helper import MONTH_MAP, WEEK_MAP, get_month, get_next_month, get_prev_month, get_day_offset

from datetime import datetime, date

def month_current(request):

    today = datetime.now().timetuple()
    cur_month, month_iter = get_month(today.tm_mon, today.tm_year)

    prev_t = get_prev_month(today.tm_year, today.tm_mon)
    next_t = get_next_month(today.tm_year, today.tm_mon)

    context = {'cur_month': today.tm_mon,
               'cur_year': today.tm_year,
               'cur_day': today.tm_mday,
               'month': cur_month,
               'month_iter': month_iter,
               'prev_year': prev_t[0],
               'prev_month': prev_t[1],
               'next_year': next_t[0],
               'next_month': next_t[1]}

    return render(request, 'diet.html', context)


def month_view(request, year, month):

    today = datetime.now().timetuple()
    cur_month, month_iter = get_month(month, year)

    prev_t = get_prev_month(year, month)
    next_t = get_next_month(year, month)

    context = {'cur_month': today.tm_mon,
               'cur_year': today.tm_year,
               'cur_day': today.tm_mday,
               'month': cur_month,
               'month_iter': month_iter,
               'prev_year': prev_t[0],
               'prev_month': prev_t[1],
               'next_year': next_t[0],
               'next_month': next_t[1]}

    return render(request, 'diet.html', context)


def day_view(request, year, month, day):

    _slug = "%d-%d-%d" % (year, month, day)

    context = {'day': NutritionDay.objects.get(day_slug=_slug),
               'prev_day': get_day_offset(year, month, day, -1),
               'next_day': get_day_offset(year, month, day, 1)}


    return render(request, 'day_details.html', context)
