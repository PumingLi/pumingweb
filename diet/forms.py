from django import forms

class FoodForm(forms.Form):

    MEALS = (("Breakfast", "Breakfast"),
                ("Lunch", "Lunch"),
                ("Dinner", "Dinner"),
                ("Snack", "Snack"),
                ("Other", "Other"),
                )
    item_name = forms.CharField(label='Item name', max_length=100)
    item_calories = forms.IntegerField(label='Item calories')
    item_carbs = forms.IntegerField(label='Item carbs')
    item_protein = forms.IntegerField(label='Item protein')
    item_fat = forms.IntegerField(label='Item fat')
    item_type = forms.ChoiceField(choices=MEALS)
