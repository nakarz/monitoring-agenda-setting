from django.shortcuts import render, get_object_or_404, redirect
from input_agenda_setting.models import InputAgendaSetting

def table_input_as(request):
    input_as_data = InputAgendaSetting.objects.all()
    total_input_as = InputAgendaSetting.objects.count()
    
    context = {
        'input_as_data': input_as_data,
        'count_total_input_as': total_input_as,
    }
    return render(request, 'table_input-as.html', context)

def edit_agenda_setting(request, id):
    agenda_setting = get_object_or_404(InputAgendaSetting, id=id)
    if request.method == 'POST':
        nomor_agenda = request.POST.get('nomor_agenda')
        topik_agenda = request.POST.get('topik_agenda')
        pesan_kunci = request.POST.get('pesan_kunci')
        sub_pesan_kunci = request.POST.get('sub_pesan_kunci')
        
        rentang_tanggal_waktu = request.POST.get('agenda_date_time')
        tanggal_awal, tanggal_akhir = rentang_tanggal_waktu.split(' to ')

        agenda_setting.nomor_agenda = nomor_agenda
        agenda_setting.topik_agenda = topik_agenda
        agenda_setting.pesan_kunci = pesan_kunci
        agenda_setting.sub_pesan_kunci = sub_pesan_kunci
        agenda_setting.agenda_date_time_start = tanggal_awal
        agenda_setting.agenda_date_time_end = tanggal_akhir
        agenda_setting.save()

        return redirect('table_input_as')
    return render(request, 'edit_input-as.html', {'agenda_setting': agenda_setting})

def delete_agenda_setting(request, nomor_agenda):
    agenda = get_object_or_404(InputAgendaSetting, nomor_agenda=nomor_agenda)
    
    if request.method == 'POST':
        agenda.delete()
        return redirect('table_input_as')
