from django.shortcuts import render
from input_agenda_setting.models import InputAgendaSetting
from socmed_data.models import *

def statistic_agenda(request):
    total_agenda_setting = InputAgendaSetting.objects.count()
    total_topik_agenda = InputAgendaSetting.objects.values_list('topik_agenda', flat=True).distinct().count()

    # Get pesan_kunci and sub_pesan_kunci from the database
    pesan_kunci = InputAgendaSetting.objects.values_list('pesan_kunci', flat=True)
    sub_pesan_kunci = InputAgendaSetting.objects.values_list('sub_pesan_kunci', flat=True)

    # Count the number of words in pesan_kunci and sub_pesan_kunci
    total_pesan_kunci_words = sum(len(pesan.split()) for pesan in pesan_kunci)
    total_sub_pesan_kunci_words = sum(len(sub_pesan.split()) for sub_pesan in sub_pesan_kunci)

    context = {
        'total_agenda_setting': total_agenda_setting,
        'total_topik_agenda': total_topik_agenda,
        'total_pesan_kunci_words': total_pesan_kunci_words,
        'total_sub_pesan_kunci_words': total_sub_pesan_kunci_words,
    }

    return render(request, 'statistic.html', context)


def db_statistic(request):
    socmed_data_list = SocialMediaData.objects.all()
    total_socmed_data = SocialMediaData.objects.count()
    total_agendas = InputAgendaSetting.objects.count()

    context = {
        'socmed_data_list': socmed_data_list,
        'total_socmed_data': total_socmed_data,
        'total_agendas': total_agendas,
    }
    return render(request, 'db_statistic.html', context)
