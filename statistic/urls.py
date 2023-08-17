from django.urls import path
from . import views

urlpatterns = [
    path('statistic/', views.statistic_agenda, name='statistic'),
    path('statistic/database', views.db_statistic, name='database'),
]
