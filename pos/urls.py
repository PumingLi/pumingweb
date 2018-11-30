from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.tagger, name='tagger'),
    path('tag_input/<str:input>', views.tag_input, name='tag_input'),
]
