from django.urls import path

from . import views

urlpatterns = [
    path('', views.diet, name='diet'),
    path('<int:day_id>/', views.day_view, name='day_view'),
    path('<str:month_slug>/', views.month_view, name='month_view')
]
