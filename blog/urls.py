from django.urls import path

from . import views

urlpatterns = [
    path('', views.blog, name='blog'),
    path('<int:id>', views.post, name='post'),
    path('vote/<int:id>/<str:vote>', views.vote, name='vote'),
    path('add_comment/<int:id>', views.add_comment, name='add_comment'),



]
