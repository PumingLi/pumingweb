from django import forms
from .constants import MEALS, EXERCISES


class FoodForm(forms.Form):

    item_name = forms.CharField(label='Name', max_length=100)
    item_calories = forms.IntegerField(label='Calories')
    item_carbs = forms.IntegerField(label='Carbs')
    item_protein = forms.IntegerField(label='Protein')
    item_fat = forms.IntegerField(label='Fat')
    item_type = forms.ChoiceField(choices=[(m, m) for m in MEALS])


class ExerciseForm(forms.Form):

    exercise_name = forms.CharField(label='Name', max_length=100)
    exercise_type = forms.ChoiceField(choices=[(e, e) for e in EXERCISES])
    exercise_sets = forms.IntegerField(label='Sets')
    exercise_reps = forms.IntegerField(label='Reps')
    exercise_weight = forms.IntegerField(label='Weight')
    exercise_time = forms.IntegerField(label='Duration')

class SearchForm(forms.Form):

    food_name = forms.CharField(label='Food Name', max_length=100)
