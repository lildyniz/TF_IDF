from django.urls import path
from . import views


app_name = 'analysis'

urlpatterns = [
    path('', views.index, name='index'),
    path('analysis/<int:id>/', views.file_to_analysis, name='file_to_analysis')
]