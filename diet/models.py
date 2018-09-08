from django.db import models


class NutritionMonth(models.Model):

    MONTHS = (
        ('January', 'January'),
        ('February', 'February'),
        ('March', 'March'),
        ('April', 'April'),
        ('May', 'May'),
        ('June', 'June'),
        ('July', 'July'),
        ('August', 'August'),
        ('September', 'September'),
        ('October', 'October'),
        ('November', 'November'),
        ('December', 'December'),
    )
    year = models.IntegerField()
    month = models.TextField(default="January", choices=MONTHS)

class NutritionWeek(models.Model):
    month = models.ForeignKey(NutritionMonth, on_delete=models.CASCADE)
    week_num = models.IntegerField(default=0)


class NutritionDay(models.Model):

    WEEKDAYS = (("Sunday", "Sunday"),
                ("Monday", "Monday"),
                ("Tuesday", "Tuesday"),
                ("Wednesday", "Wednesday"),
                ("Thursday", "Thursday"),
                ("Friday", "Friday"),
                ("Saturday", "Saturday"),
                )
    week = models.ForeignKey(NutritionWeek, on_delete=models.CASCADE)
    weekday = models.TextField(default="Sunday", choices=WEEKDAYS)
    cur_date = models.DateField()
    calories = models.IntegerField(default=0)
    carb = models.IntegerField(default=0)
    protein = models.IntegerField(default=0)
    fat = models.IntegerField(default=0)
    weight = models.IntegerField(null=True)
