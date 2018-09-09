from django.urls import path

from . import views

urlpatterns = [
    path('current', views.month_current, name='diet_month_current'),
    path('<int:year>/<int:month>/<int:day>', views.day_view, name='day_view'),
    path('<int:year>/<int:month>', views.month_view, name='month_view')
]
