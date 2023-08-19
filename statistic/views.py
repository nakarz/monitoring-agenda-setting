from django.shortcuts import render, get_object_or_404
from input_agenda_setting.models import InputAgendaSetting
from similarity_checker.views import calculate_similarity
from socmed_data.models import *
from socmed_data.utils import scrape_instagram_data_api

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

def statistic_agenda_ue1(request, ue1):
    total_agenda_setting = InputAgendaSetting.objects.count()
    total_topik_agenda = InputAgendaSetting.objects.values_list('topik_agenda', flat=True).distinct().count()

    # Get pesan_kunci and sub_pesan_kunci from the database
    pesan_kunci = InputAgendaSetting.objects.values_list('pesan_kunci', flat=True)
    sub_pesan_kunci = InputAgendaSetting.objects.values_list('sub_pesan_kunci', flat=True)

    # Count the number of words in pesan_kunci and sub_pesan_kunci
    total_pesan_kunci_words = sum(len(pesan.split()) for pesan in pesan_kunci)
    total_sub_pesan_kunci_words = sum(len(sub_pesan.split()) for sub_pesan in sub_pesan_kunci)

    agenda_setting = get_object_or_404(InputAgendaSetting)
    agenda_start = agenda_setting.agenda_date_time_start
    agenda_end = agenda_setting.agenda_date_time_end

    account_data = []

    # Get all unique account URLs for the specified UE1
    account_urls = SocialMediaData.objects.filter(ue1=ue1).values_list('account_url', flat=True).distinct()

    total_similarity = 0
    total_entries = 0

    for account_url in account_urls:
        scraped_data = scrape_instagram_data_api(account_url, agenda_start, agenda_end)
        captions = scraped_data.get('captions', [])
        likes = scraped_data.get('likes', [])
        comments = scraped_data.get('comments', [])
        viewers = scraped_data.get('viewers', [])
        post_urls = scraped_data.get('post_urls', [])
        followers = scraped_data.get('followers', [])
        posts = scraped_data.get('posts', 0)

        similarity_values = []

        account_info = {
            'account_url': account_url,
            'social_media': 'Instagram',  # Update this as needed
            'ue1': ue1,
            'posts': posts,
            'followers': followers,
            'account_data': [],
        }

        account_data_entries = []

        for post_url, caption, viewer, comment, like in zip(post_urls, captions, viewers, comments, likes):
            similarity = calculate_similarity(caption, agenda_setting.pesan_kunci, agenda_setting.sub_pesan_kunci)
            similarity_values.append(similarity)
            
            entry = {
                'post_url': post_url,
                'caption': caption,
                'viewer': viewer,
                'comment': comment,
                'like': like,
                'similarity': similarity,
                'status_similarity': 'Sesuai' if similarity != 0.0 else 'Tidak Sesuai',
            }
            account_data_entries.append(entry)

            total_similarity += similarity
            total_entries += 1

        account_info['account_data'] = account_data_entries
        account_data.append(account_info)

    average_similarity = total_similarity / total_entries if total_entries > 0 else 0

    # Count total posts and posts matching agenda setting
    total_posts, posts_matching_agenda = count_posts(account_data)

    context = {
        'ue1': ue1,
        'agenda_start': agenda_start,
        'agenda_end': agenda_end,
        'account_data': account_data,
        'average_similarity': average_similarity,
        'total_posts': total_posts,
        'posts_matching_agenda': posts_matching_agenda,
        'total_agenda_setting': total_agenda_setting,
        'total_topik_agenda': total_topik_agenda,
        'total_pesan_kunci_words': total_pesan_kunci_words,
        'total_sub_pesan_kunci_words': total_sub_pesan_kunci_words,
    }

    return render(request, 'statistic_ue1.html', context)

def count_posts(account_data):
    total_posts = 0
    posts_matching_agenda = 0

    for account_info in account_data:
        total_posts += account_info['posts']
        for entry in account_info['account_data']:
            similarity = entry['similarity']
            if similarity > 0.0:
                posts_matching_agenda += 1

    return total_posts, posts_matching_agenda


