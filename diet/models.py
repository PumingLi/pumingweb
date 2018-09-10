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
    month_num = models.IntegerField(default=1, choices=[(d, d) for d in range(1, 13)])
    month_slug = models.TextField(default="00-00")

class NutritionDay(models.Model):

    WEEKDAYS = (("Sunday", "Sunday"),
                ("Monday", "Monday"),
                ("Tuesday", "Tuesday"),
                ("Wednesday", "Wednesday"),
                ("Thursday", "Thursday"),
                ("Friday", "Friday"),
                ("Saturday", "Saturday"),
                )
    month = models.ForeignKey(NutritionMonth, on_delete=models.CASCADE)
    day_slug = models.TextField(default="00-00-00")
    weekday = models.TextField(default="Sunday", choices=WEEKDAYS)
    cur_date = models.DateField()
    calories = models.IntegerField(default=0)
    carb = models.IntegerField(default=0)
    protein = models.IntegerField(default=0)
    fat = models.IntegerField(default=0)
    weight = models.IntegerField(null=True)

class FoodItem(models.Model):

    MEALS = (("Breakfast", "Breakfast"),
                ("Lunch", "Lunch"),
                ("Dinner", "Dinner"),
                ("Snack", "Snack"),
                ("Other", "Other"),
                )
    day = models.ForeignKey(NutritionDay, on_delete=models.CASCADE)
    name = models.TextField(default="N/A")
    type = models.TextField(default="Snack", choices=MEALS)
    calories = models.IntegerField(default=0)
    carb = models.IntegerField(default=0)
    protein = models.IntegerField(default=0)
    fat = models.IntegerField(default=0)
