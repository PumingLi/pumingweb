from django.urls import path

from . import views

urlpatterns = [
    path('current', views.month_current, name='diet_month_current'),
    path('<int:year>/<int:month>/<int:day>', views.day_view, name='day_view'),
    path('<int:year_a>/<int:month_a>/<int:day_a>/<str:slug>/add-food', views.add_food, name='add_food'),
    path('<int:year>/<int:month>', views.month_view, name='month_view')
]
