from .models import NutritionDay, NutritionWeek, NutritionMonth
from datetime import datetime, date
import calendar

MONTH_MAP = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
WEEK_MAP = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

def get_prev_month(cur_month, cur_year):

    if cur_month == 1:
        return '12-%d' % (cur_year-1)
    else:
        return '%d-%d' % (cur_month-1, cur_year)

def get_next_month(cur_month, cur_year):

    if cur_month == 12:
        return '1-%d' % (cur_year+1)
    else:
        return '%d-%d' % (cur_month+1, cur_year)

def get_month(month, year):


    if len(NutritionMonth.objects.filter(year=year).filter(month=MONTH_MAP[month-1])) > 0:
        cur_month = NutritionMonth.objects.filter(year=year).get(month=MONTH_MAP[month-1])
    else:
        cur_month = NutritionMonth(year=year, month=MONTH_MAP[month-1], month_num=month)
        cur_month.save()

        month_iter = calendar.Calendar().itermonthdates(year, month)
        count = 0
        w_num = 0
        for day in month_iter:

            if count%7 == 0:
                count = 0
                w_num += 1
                cur_week = NutritionWeek(month=cur_month, week_num=w_num)
                cur_week.save()

            _day_t = day.timetuple()
            cur_day = NutritionDay(week=cur_week, cur_date=date(_day_t.tm_year, _day_t.tm_mon, _day_t.tm_mday), weekday=WEEK_MAP[count])
            cur_day.save()

            count+=1

    return cur_month
