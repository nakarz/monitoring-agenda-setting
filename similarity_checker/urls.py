from django.urls import path
from . import views

urlpatterns = [
    path('similarity-checker/', views.similarity_checker, name='similarity-checker'),
    path('dashboard-similarity-checker/', views.dashboard_similarity_checker, name='dashboard_similarity_checker'),
    path('agenda-accuracy/<str:ue1>/', views.agenda_accuracy, name='agenda_accuracy'),
    path('download-agenda-accuracy/<str:ue1>/', views.download_agenda_accuracy, name='download_agenda_accuracy'),
]