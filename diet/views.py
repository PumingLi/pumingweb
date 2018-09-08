from django.shortcuts import render

from .models import NutritionDay, NutritionWeek, NutritionMonth
from .helper import MONTH_MAP, WEEK_MAP, get_month, get_next_month, get_prev_month

from datetime import datetime, date

def diet(request):

    today = datetime.now().timetuple()
    cur_month = get_month(today.tm_mon, today.tm_year)
    context = {'cur_month': MONTH_MAP[today.tm_mon-1],
               'cur_year': today.tm_year,
               'cur_day': today.tm_mday,
               'month': cur_month,
               'prev_url': get_prev_month(today.tm_mon, today.tm_year),
               'next_url': get_next_month(today.tm_mon, today.tm_year)}

    return render(request, 'diet.html', context)


def month_view(request, month_slug):

    today = datetime.now().timetuple()
    slug_array = month_slug.split('-')

    month_num = int(slug_array[0])
    year = int(slug_array[1])

    month = get_month(month_num, year)
    context = {'cur_month': MONTH_MAP[month_num-1],
               'cur_year': year,
               'cur_day': today.tm_mday,
               'month': month,
               'prev_url': get_prev_month(month_num, year),
               'next_url': get_next_month(month_num, year)}

    return render(request, 'diet.html', context)


def day_view(request, day_id):
    context = {'day': NutritionDay.objects.get(id=day_id)}

    return render(request, 'day_details.html', context)
