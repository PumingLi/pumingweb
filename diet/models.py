from django.db import models
from .constants import MEALS, EXERCISES, MONTH_MAP, WEEK_MAP


class NutritionMonth(models.Model):

    year = models.IntegerField()
    month = models.TextField(default="January", choices=[(m,m) for m in MONTH_MAP])
    month_num = models.IntegerField(default=1, choices=[(d, d) for d in range(1, 13)])
    month_slug = models.TextField(default="00-00")

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

class FoodItem(models.Model):

    day = models.ForeignKey(NutritionDay, on_delete=models.CASCADE)
    name = models.TextField(default="N/A")
    type = models.TextField(default="Snack", choices=[(m,m) for m in MEALS])
    calories = models.IntegerField(default=0)
    carbs = models.IntegerField(default=0)
    protein = models.IntegerField(default=0)
    fat = models.IntegerField(default=0)

class ExerciseItem(models.Model):

    day = models.ForeignKey(NutritionDay, on_delete=models.CASCADE)
    name = models.TextField(default="N/A")
    type = models.TextField(default="Push", choices=[(e,e) for e in EXERCISES])
    reps = models.IntegerField(default=0)
    sets = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)
    time = models.IntegerField(default=0)
