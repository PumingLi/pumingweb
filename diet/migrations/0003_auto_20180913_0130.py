# Generated by Django 2.1 on 2018-09-13 08:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diet', '0002_fooditem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fooditem',
            old_name='carb',
            new_name='carbs',
        ),
        migrations.RenameField(
            model_name='nutritionday',
            old_name='carb',
            new_name='carbs',
        ),
    ]