from django.contrib import admin
from .models import NutritionDay, NutritionMonth, FoodItem, ExerciseItem

admin.site.register(NutritionDay)
admin.site.register(NutritionMonth)
admin.site.register(FoodItem)
admin.site.register(ExerciseItem)
