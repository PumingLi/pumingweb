from django.shortcuts import render, redirect

from .models import NutritionDay, NutritionMonth, FoodItem, ExerciseItem
from .helper import get_food_list
from .constants import  MONTH_MAP, WEEK_MAP, PASTEL_COLORS, DAILY_SERVINGS
from .forms import FoodForm, ExerciseForm, SearchForm
from time import gmtime, strftime
from datetime import datetime, date
import calendar, json

DAILY_SCALED = {k:(DAILY_SERVINGS[k])/100 for k in DAILY_SERVINGS}


def month_current(request):

    today = datetime.now().timetuple()

    _month_slug = "%d-%d" % (today.tm_year, today.tm_mon)
    print(_month_slug)
    if not NutritionMonth.objects.filter(month_slug=_month_slug):
        cur_month = NutritionMonth(year=today.tm_year,
                                   month=MONTH_MAP[today.tm_mon-1],
                                   month_num=today.tm_mon,
                                   month_slug=_month_slug)
        cur_month.save()
    else:
        cur_month = NutritionMonth.objects.get(month_slug=_month_slug)

    month_iter = cur_month.get_month_iter()
    pastel_array = list(PASTEL_COLORS.values())

    prev_year, prev_month = cur_month.get_month_offset(-1)
    next_year, next_month = cur_month.get_month_offset(1)

    cur_month.fill_month()

    context = {'cur_month': today.tm_mon,
               'cur_year': today.tm_year,
               'cur_day': today.tm_mday,
               'month': cur_month,
               'month_iter': month_iter,
               'prev_year': prev_year,
               'prev_month': prev_month,
               'next_year': next_year,
               'next_month': next_month,
               'pastel_array': pastel_array[::-1],
               'daily_p': DAILY_SCALED}


    return render(request, 'diet.html', context)


def month_view(request, year, month):

    today = datetime.now().timetuple()

    _month_slug = "%d-%d" % (year, month)
    if not NutritionMonth.objects.filter(month_slug=_month_slug):
        cur_month = NutritionMonth(year=year,
                                   month=MONTH_MAP[month-1],
                                   month_num=month,
                                   month_slug=_month_slug)
        cur_month.save()
    else:
        cur_month = NutritionMonth.objects.get(month_slug=_month_slug)

    pastel_array = list(PASTEL_COLORS.values())

    prev_year, prev_month = cur_month.get_month_offset(-1)
    next_year, next_month = cur_month.get_month_offset(1)


    context = {'cur_month': today.tm_mon,
               'cur_year': today.tm_year,
               'cur_day': today.tm_mday,
               'month': cur_month,
               'month_iter': cur_month.get_month_iter(),
               'prev_year': prev_year,
               'prev_month': prev_month,
               'next_year': next_year,
               'next_month': next_month,
               'pastel_array': pastel_array[::-1],
               'daily_p': DAILY_SCALED}


    return render(request, 'diet.html', context)


def day_view(request, year, month, day):

    _slug = "%d-%d-%d" % (year, month, day)
    cur_day = NutritionDay.objects.get(day_slug=_slug)
    day_items = cur_day.fooditem_set.all()
    day_exercises = cur_day.exerciseitem_set.all()

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

    calories_data = json.dumps({'calories_data': calories_array}).replace('\\', '\\\\').replace("'", "\\'")
    carbs_data = json.dumps({'carbs_data': carbs_array}).replace('\\', '\\\\').replace("'", "\\'")
    protein_data = json.dumps({'protein_data': protein_array}).replace('\\', '\\\\').replace("'", "\\'")
    fat_data = json.dumps({'fat_data': fat_array}).replace('\\', '\\\\').replace("'", "\\'")


    context = {'day': cur_day,
               'prev_day': cur_day.get_day_offset(-1),
               'next_day': cur_day.get_day_offset(1),
               'calories_data': calories_data,
               'carbs_data': carbs_data,
               'protein_data': protein_data,
               'fat_data': fat_data,
               'pastel_colors': pastel_colors,
               'day_items': day_items,
               'push_exercise': day_exercises.filter(type="Push"),
               'pull_exercise': day_exercises.filter(type="Pull"),
               'legs_exercise': day_exercises.filter(type="Legs"),
               'cardio_exercise': day_exercises.filter(type="Cardio"),
               'food_form': FoodForm(),
               'exercise_form': ExerciseForm(),
               'search_form': SearchForm(),
               'pastel_array': pastel_array[::-1],
               'enumerate_items': range(0, len(day_items)),
               'daily_p': DAILY_SCALED}

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
        item = ExerciseItem(name=f.cleaned_data['exercise_name'],
                            type=f.cleaned_data['exercise_type'],
                            reps=f.cleaned_data['exercise_reps'],
                            sets=f.cleaned_data['exercise_sets'],
                            weight=f.cleaned_data['exercise_weight'],
                            time=f.cleaned_data['exercise_time'])
        item.save()
        item.days.add(cur_day)
        item.save()
        
    return redirect('day_view', year=year_a, month=month_a, day=day_a)

def food_search(request, slug, query, meal):
    foods, error = get_food_list(query)
    context = {'query': query,
               'foods': foods,
               'error': error,
               'slug': slug,
               'meal': meal}

    return render(request, 'food_search.html', context=context)

def add_food_api(request, slug, name, brand, calories, carbs, protein, fat, meal):

    cur_day = NutritionDay.objects.get(day_slug=slug)
    cur_day.add_new_food_to_day(name, brand, calories, carbs, protein, fat, meal)
    return redirect('day_view', year=cur_day.cur_date.year, month=cur_day.cur_date.month, day=cur_day.cur_date.day)
