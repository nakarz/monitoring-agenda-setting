from django.urls import path
from . import views

urlpatterns = [
    path('data-input-agenda-setting/', views.table_input_as, name='table_input_as'),
    path('edit-agenda-setting/<int:id>', views.edit_agenda_setting, name='edit_agenda_setting'),
    path('delete/<int:nomor_agenda>/', views.delete_agenda_setting, name='delete_agenda_setting'),
]
