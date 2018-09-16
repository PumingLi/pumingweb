from django.urls import path

from . import views

urlpatterns = [
    path('current', views.month_current, name='diet_month_current'),
    path('<int:year>/<int:month>/<int:day>', views.day_view, name='day_view'),
    path('<int:year_a>/<int:month_a>/<int:day_a>/<str:slug>/add-food', views.add_food, name='add_food'),
    path('<int:year_a>/<int:month_a>/<int:day_a>/<str:slug>/add-exercise', views.add_exercise, name='add_exercise'),
    path('<int:year>/<int:month>', views.month_view, name='month_view'),
    path('food-search/<str:slug>/<str:query>/<str:meal>', views.food_search, name='food_search'),
    path('add-food-api/<str:slug>/<str:name>/<str:brand>/<int:calories>/<int:carbs>/<int:protein>/<int:fat>/<str:meal>', views.add_food_api, name='add_food_api'),
]
