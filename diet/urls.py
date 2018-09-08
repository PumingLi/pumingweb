from django.urls import path

from . import views

urlpatterns = [
    path('', views.diet, name='diet'),
    path('<int:day_id>/', views.day_details, name='day details'),
]
