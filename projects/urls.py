from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.projects, name='projects'),
    path('pos/', include('pos.urls')),
    path('bayes/', include('bayes.urls')),
]
