from django.db import models
from .helper import get_food_list
from .constants import MEALS, EXERCISES, MONTH_MAP, WEEK_MAP, RAND_FOODS
from datetime import datetime, date, timedelta
import calendar, math, random

class NutritionMonth(models.Model):

    year = models.IntegerField()
    month = models.TextField(default="January", choices=[(m,m) for m in MONTH_MAP])
    month_num = models.IntegerField(default=1, choices=[(d, d) for d in range(1, 13)])
    month_slug = models.TextField(default="00-00")

    def __str__(self):
        return 'NutritionMonth: %s' % (self.month_slug)

    def get_month_offset(self, delta):

        month = ((self.month_num-1) + delta)%12 + 1
        years_delta = -1*int(delta/12) if delta < 0 else int(delta/12)

        if self.month_num + delta < 1:
            years_delta -= 1
        elif self.month_num + delta > 12:
            years_delta += 1
            
        year = self.year + years_delta
        _month_slug = "%d-%d" % (year, month)
        if not NutritionMonth.objects.filter(month_slug=_month_slug):
            new_month = NutritionMonth(year=year,
                                       month=MONTH_MAP[month-1],
                                       month_num=month,
                                       month_slug=_month_slug)
            new_month.save()
        return year, month

    def get_month_iter(self):

        month_iter = []
        month_cal = calendar.Calendar().itermonthdates(self.year, self.month_num)
        count = 0
        week_iter = []
        for day in month_cal:

            _day_t = day.timetuple()
            _slug = "%d-%d-%d" % (_day_t.tm_year, _day_t.tm_mon, _day_t.tm_mday)
            if NutritionDay.objects.filter(day_slug=_slug):
                cur_day = NutritionDay.objects.get(day_slug=_slug)
            else:
                cur_day = NutritionDay(month=self,
                                       cur_date=date(_day_t.tm_year, _day_t.tm_mon, _day_t.tm_mday),
                                       weekday=WEEK_MAP[count],
                                       day_slug=_slug)
                cur_day.save()
            count+=1
            week_iter.append(cur_day)

            if count%7 == 0:
                count = 0
                month_iter.append(week_iter)
                week_iter = []

        return month_iter


    def fill_month(self, day=None):
        random.seed(int(datetime.now().timestamp()))
        past_foods = list(FoodItem.objects.all())
        past_exercise = list(ExerciseItem.objects.all())
        month_days = self.nutritionday_set.filter(cur_date__month=self.month_num)
        for d in range(1, date.today().day + 1):
            day = month_days.get(cur_date__day=d)
            if not day.fooditem_set.all():

                for f in random.sample(past_foods, k=random.randrange(4, 8)):
                    f.copy_to_date(day)

                for e in random.sample(past_exercise, k=random.randrange(0, 6)):
                    e.copy_to_date(day)


class NutritionDay(models.Model):

    month = models.ForeignKey(NutritionMonth, on_delete=models.CASCADE)
    day_slug = models.TextField(default="00-00-00")
    weekday = models.TextField(default="Sunday", choices=[(w,w) for w in WEEK_MAP])
    cur_date = models.DateField()
    calories = models.IntegerField(null=True)
    carbs = models.IntegerField(null=True)
    protein = models.IntegerField(null=True)
    fat = models.IntegerField(null=True)
    weight = models.IntegerField(null=True)

    def __str__(self):
        return 'NutritionDay: %s' % (self.day_slug)

    def add_new_food_to_day(self, name, brand, calories, carbs, protein, fat, meal):

        self.calories += calories
        self.carbs += carbs
        self.protein += protein
        self.fat += fat
        self.save()

        item = FoodItem(day=self,
                        name="{} ({})".format(name.replace("%2F", "/"), brand.replace("%2F", "/")),
                        type=meal,
                        calories=calories,
                        carbs=carbs,
                        protein=protein,
                        fat=fat)
        item.save()

    def get_day_offset(self, delta):

        offset_date = self.cur_date + timedelta(days=delta)

        _month_slug = "%d-%d" % (offset_date.year, offset_date.month)
        month = NutritionMonth.objects.filter(month_slug=_month_slug)
        if month:
            month = month[0]
        else:
            month = NutritionMonth(year=offset_date.year,
                                   month=MONTH_MAP[offset_date.month-1],
                                   month_num=offset_date.month,
                                   month_slug=_month_slug)
            month.save()

        _slug = "%d-%d-%d" % (offset_date.year, offset_date.month, offset_date.day)
        if not NutritionDay.objects.filter(day_slug=_slug):
            day = NutritionDay(month=month,
                               cur_date=self.cur_date,
                               weekday=WEEK_MAP[offset_date.timetuple().tm_wday],
                               day_slug=_slug)
            day.save()

        print(offset_date)
        return (offset_date.year, offset_date.month, offset_date.day)

    def update_nutrients(self):
        self.calories = 0
        self.carbs = 0
        self.protein = 0
        self.fat = 0
        for food in self.fooditem_set.all():
            self.calories += food.calories
            self.carbs += food.carbs
            self.protein += food.protein
            self.fat += food.fat
        self.save()


class FoodItem(models.Model):

    day = models.ForeignKey(NutritionDay, on_delete=models.CASCADE)
    name = models.TextField(default="N/A")
    type = models.TextField(default="Snack", choices=[(m,m) for m in MEALS])
    calories = models.IntegerField(default=0)
    carbs = models.IntegerField(default=0)
    protein = models.IntegerField(default=0)
    fat = models.IntegerField(default=0)

    def __str__(self):
        return 'FoodItem: %s (%s)' % (self.name, self.day.day_slug)

    def copy_to_date(self, date):

        date.calories += calories
        date.carbs += carbs
        date.protein += protein
        date.fat += fat
        date.save()

        new_food = FoodItem(day=date,
                            name=self.name,
                            type=self.type,
                            calories=self.calories,
                            carbs=self.carbs,
                            protein=self.protein,
                            fat=self.fat)

        new_food.save()
        return new_food



class ExerciseItem(models.Model):

    day = models.ForeignKey(NutritionDay, on_delete=models.CASCADE)
    name = models.TextField(default="N/A")
    type = models.TextField(default="Push", choices=[(e,e) for e in EXERCISES])
    reps = models.IntegerField(default=0)
    sets = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)
    time = models.IntegerField(default=0)

    def __str__(self):
        return 'ExerciseItem: %s (%s)' % (self.name, self.day.day_slug)

    def copy_to_date(self, date):

        new_exer = ExerciseItem(day=date,
                                name=self.name,
                                type=self.type,
                                reps=self.reps,
                                sets=self.sets,
                                weight=self.weight,
                                time=self.time)

        new_exer.save()
        return new_exer
