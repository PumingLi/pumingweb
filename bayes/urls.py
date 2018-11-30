from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.bayes, name='bayes'),
    path('classify_input/<str:input>', views.classify_input, name='classify'),

]
