from django.shortcuts import render, redirect

from .models import NutritionDay, NutritionMonth, FoodItem, ExerciseItem
from .helper import get_month, get_next_month, get_prev_month, get_day_offset
from .constants import  MONTH_MAP, WEEK_MAP, PASTEL_COLORS, DAILY_SERVINGS
from .forms import FoodForm, ExerciseForm

from datetime import datetime, date

import json

DAILY_SCALED = {k:(DAILY_SERVINGS[k])/100 for k in DAILY_SERVINGS}


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
               'next_month': next_t[1],
               'daily_p': DAILY_SCALED}


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
               'next_month': next_t[1],
               'daily_p': DAILY_SCALED}

    return render(request, 'diet.html', context)


def day_view(request, year, month, day):

    _slug = "%d-%d-%d" % (year, month, day)
    cur_day = NutritionDay.objects.get(day_slug=_slug)
    day_items = FoodItem.objects.filter(day=cur_day)

    pastel_len = len(PASTEL_COLORS)
    pastel_array = list(PASTEL_COLORS.values())

    pastel_colors = json.dumps({x:{'color': pastel_array[pastel_len-1-x]} for x in range(0, pastel_len)})

    calories_array = [['Name', 'Calories']]
    carbs_array = [['Name', 'Carbs']]
    protein_array = [['Name', 'Protein']]
    fat_array = [['Name', 'Fat']]

    for item in day_items:
        calories_array.append([item.name, item.calories])
        carbs_array.append([item.name, item.carbs])
        protein_array.append([item.name, item.protein])
        fat_array.append([item.name, item.fat])

    calories_data = json.dumps({'calories_data': calories_array})
    carbs_data = json.dumps({'carbs_data': carbs_array})
    protein_data = json.dumps({'protein_data': protein_array})
    fat_data = json.dumps({'fat_data': fat_array})


    context = {'day': cur_day,
               'prev_day': get_day_offset(year, month, day, -1),
               'next_day': get_day_offset(year, month, day, 1),
               'calories_data': calories_data,
               'carbs_data': carbs_data,
               'protein_data': protein_data,
               'fat_data': fat_data,
               'pastel_colors': pastel_colors,
               'day_items': day_items,
               'push_exercise': ExerciseItem.objects.filter(day=cur_day).filter(type="Push"),
               'pull_exercise': ExerciseItem.objects.filter(day=cur_day).filter(type="Pull"),
               'legs_exercise': ExerciseItem.objects.filter(day=cur_day).filter(type="Legs"),
               'cardio_exercise': ExerciseItem.objects.filter(day=cur_day).filter(type="Cardio"),
               'food_form': FoodForm(),
               'exercise_form': ExerciseForm()}

    return render(request, 'day_details.html', context)



def add_food(request, year_a, month_a, day_a, slug):

    f = FoodForm(request.POST)
    if f.is_valid():
        cur_day = NutritionDay.objects.get(day_slug=slug)
        cur_day.calories += f.cleaned_data['item_calories']
        cur_day.carbs += f.cleaned_data['item_carbs']
        cur_day.protein += f.cleaned_data['item_protein']
        cur_day.fat += f.cleaned_data['item_fat']
        cur_day.save()

        item = FoodItem(day=cur_day,
                        name=f.cleaned_data['item_name'],
                        type=f.cleaned_data['item_type'],
                        calories=f.cleaned_data['item_calories'],
                        carbs=f.cleaned_data['item_carbs'],
                        protein=f.cleaned_data['item_protein'],
                        fat=f.cleaned_data['item_fat'])
        item.save()

    return redirect('day_view', year=year_a, month=month_a, day=day_a)

def add_exercise(request, year_a, month_a, day_a, slug):

    f = ExerciseForm(request.POST)
    if f.is_valid():
        cur_day = NutritionDay.objects.get(day_slug=slug)
        item = ExerciseItem(day=cur_day,
                            name=f.cleaned_data['exercise_name'],
                            type=f.cleaned_data['exercise_type'],
                            reps=f.cleaned_data['exercise_reps'],
                            sets=f.cleaned_data['exercise_sets'],
                            time=f.cleaned_data['exercise_time'])
        item.save()

    return redirect('day_view', year=year_a, month=month_a, day=day_a)
