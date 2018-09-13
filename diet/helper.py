from .models import NutritionDay, NutritionMonth
from datetime import datetime, date, timedelta
import calendar

MONTH_MAP = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
WEEK_MAP = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

PASTEL_COLORS = {
"Snow": "#fffafa",
"Snow 2": "#eee9e9",
"Snow 3": "#cdc9c9",
"Snow 4": "#8b8989",
"Ghost White": "#f8f8ff",
"White Smoke": "#f5f5f5",
"Gainsboro": "#dccdc",
"Floral White": "#fffaf0",
"Old Lace": "#fdf5e6",
"Linen": "#faf0e6",
"Antique White": "#faebd7",
"Antique White 2": "#eedfcc",
"Antique White 3": "#cdc0b0",
"Antique White 4": "#8b8378",
"Papaya Whip": "#ffefd5",
"Blanched Almond": "#ffebcd",
"Bisque": "#ffe4c4",
"Bisque 2": "#eed5b7",
"Bisque 3": "#cdb79e",
"Bisque 4": "#8b7d6b",
"Peach Puff": "#ffdab9",
"Peach Puff 2": "#eecbad",
"Peach Puff 3": "#cdaf95",
"Peach Puff 4": "#8b7765",
"Navajo White": "#ffdead",
"Moccasin": "#ffe4b5",
"Cornsilk": "#fff8dc",
"Cornsilk 2": "#eee8dc",
"Cornsilk 3": "#cdc8b1",
"Cornsilk 4": "#8b8878",
"Ivory": "#fffff0",
"Ivory 2": "#eeeee0",
"Ivory 3": "#cdcdc1",
"Ivory 4": "#8b8b83",
"Lemon Chiffon": "#fffacd",
"Seashell": "#fff5ee",
"Seashell 2": "#eee5de",
"Seashell 3": "#cdc5bf",
"Seashell 4": "#8b8682",
"Honeydew": "#f0fff0",
"Honeydew 2": "#e0eee0",
"Honeydew 3": "#c1cdc1",
"Honeydew 4": "#838b83",
"Mint Cream": "#f5fffa",
"Azure": "#f0ffff",
"Alice Blue": "#f0f8ff",
"Lavender": "#e6e6fa",
"Lavender Blush": "#fff0f5",
"Misty Rose": "#ffe4e1"
}

DAILY_SERVINGS = {
'CALORIES': 2500,
'PROTEIN': 150,
'CARBS': 180,
'FAT': 120}


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
