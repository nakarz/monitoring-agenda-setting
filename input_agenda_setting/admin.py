from django.contrib import admin
from .models import InputAgendaSetting

@admin.register(InputAgendaSetting)
class InputAgendaSettingAdmin(admin.ModelAdmin):
    list_display = ('id', 'nomor_agenda', 'topik_agenda', 'agenda_date_time_start', 'agenda_date_time_end', 'pesan_kunci', 'sub_pesan_kunci')
    search_fields = ('id', 'nomor_agenda', 'topik_agenda', 'pesan_kunci', 'sub_pesan_kunci')
    list_filter = ('id', 'agenda_date_time_start', 'agenda_date_time_end',)
