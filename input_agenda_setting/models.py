from django.db import models
from django.utils import timezone

class InputAgendaSetting(models.Model):
    nomor_agenda = models.IntegerField()
    topik_agenda = models.CharField(max_length=200)
    pesan_kunci = models.TextField()
    sub_pesan_kunci = models.TextField()
    agenda_date_time_start = models.DateTimeField(default=timezone.now)
    agenda_date_time_end = models.DateTimeField()

    def __str__(self):
        return f"Agenda Setting {self.nomor_agenda}: {self.topik_agenda}"
