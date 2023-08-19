from django.urls import path
from . import views

urlpatterns = [
    path('statistic/', views.statistic_agenda, name='statistic'),
    path('statistic/<str:ue1>/', views.statistic_agenda_ue1, name='statistic-ue1'),
    path('statistic/database', views.db_statistic, name='database'),
]
