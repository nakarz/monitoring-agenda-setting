from bs4 import BeautifulSoup
import datetime
import re
import instaloader
import urllib.parse
import pytz
import requests

"""
INSTAGRAM WEB SCRAP
"""
def convert_followers_count(count_str):
    # Remove commas from the count string
    count_str = count_str.replace(',', '')

    # Use regular expression to extract the numeric part and the multiplier (e.g., 'M')
    match = re.match(r'^([\d.]+)([KkMm]?)$', count_str)
    if match:
        count, multiplier = match.groups()
        count = float(count)
        if multiplier.lower() == 'k':
            count *= 1000
        elif multiplier.lower() == 'm':
            count *= 1000000
        return format_followers_count(int(count))
    else:
        raise ValueError(f"Invalid followers count string: {count_str}")

def format_followers_count(count):
    if count >= 1000000:
        return f"{count / 1000000:.1f}M"
    elif count >= 1000:
        return f"{count / 1000:.1f}K"
    else:
        return str(count)

def scrape_instagram_data_webscrap(account_url, agenda_start, agenda_end):
    # Extract username from account URL
    parsed_url = account_url.strip('/').split('/')[-1]
    username = parsed_url.split('/')[-1]

    # Make a request to the Instagram account's profile page
    response = requests.get(account_url)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.content, 'html.parser')


    # Extract followers count
    followers_count_str = soup.find('meta', {'property': 'og:description'}).get('content').split()[0]
    followers_count = convert_followers_count(followers_count_str)
    
    if response.status_code == 200:
        page_content = response.content.decode('utf-8')

        # Extract posts count using regular expression
        posts_count_match = re.search(r'(\d+,\d+) posts', page_content)
        if posts_count_match:
            posts_count_str = posts_count_match.group(1).replace(',', '')
            posts_count = int(posts_count_str)
        else:
            posts_count = 0
            print("Unable to get posts count")
    else:
        print(f"Failed to fetch Instagram page: {response.status_code}")

    post_urls = []
    captions = []
    likes = []
    comments = []
    viewers = []

    # Loop through the posts to extract data
    for post in soup.find_all('div', {'class': 'v1Nh3'}):
        post_url = f"https://www.instagram.com{post.find('a')['href']}"
        post_response = requests.get(post_url)
        if post_response.status_code != 200:
            continue

        post_soup = BeautifulSoup(post_response.content, 'html.parser')
        
        # Extract caption
        caption = post_soup.find('div', {'class': 'C4VMK'}).find('span').text if post_soup.find('div', {'class': 'C4VMK'}) else ''
        captions.append(caption.strip())

        # Extract likes count
        likes_count = int(post_soup.find('span', {'class': 'zV_Nj'}).text.replace(',', ''))

        # Extract comments count
        comments_count = int(post_soup.find('span', {'class': 'gU-Ip'}).text.replace(',', ''))

        # Extract viewers count
        viewers_count = None
        video_views = post_soup.find('span', {'class': 'vcOH2'})
        if video_views:
            viewers_count = int(video_views.get('title').replace(',', ''))

        post_date_utc = datetime.utcfromtimestamp(int(post.find('time')['datetime'])).replace(tzinfo=pytz.UTC)
        
        if agenda_start <= post_date_utc <= agenda_end:
            post_urls.append(post_url)
            likes.append(likes_count)
            comments.append(comments_count)
            viewers.append(viewers_count)

    scraped_data = {
        'followers': followers_count,
        'posts': posts_count,
        'post_urls': post_urls,
        'captions': captions,
        'likes': likes,
        'comments': comments,
        'viewers': viewers,
    }
    return scraped_data


"""
INSTAGRAM API LIBRARY
"""
def fetch_and_process_batch(loader, profile, agenda_start, agenda_end, batch_size=10):
    post_urls = []
    captions = []
    likes = []
    comments = []
    viewers = []

    posts = profile.get_posts()
    
    for post in posts:
        post_date_utc = post.date.astimezone(pytz.UTC)
        if post_date_utc <= agenda_end and post_date_utc >= agenda_start:
            captions.append(post.caption)
            likes.append(post.likes)
            comments.append(post.comments)
            viewers.append(post.video_view_count if post.is_video else None)
            post_urls.append(f"https://www.instagram.com/p/{post.shortcode}")

            if len(post_urls) >= batch_size:
                break

    return post_urls, captions, likes, comments, viewers

def scrape_instagram_data_api(account_url, agenda_start, agenda_end, batch_size=10):
    parsed_url = urllib.parse.urlparse(account_url)
    username = parsed_url.path.strip('/')
    loader = instaloader.Instaloader()

    try:
        profile = instaloader.Profile.from_username(loader.context, username)
    except instaloader.exceptions.ProfileNotExistsException:
        # Handle profile not found
        return {
            'followers': 0,
            'posts': 0,
            'post_urls': [],
            'captions': [],
            'likes': [],
            'comments': [],
            'viewers': [],
        }

    # Fetch and process data in batches
    post_urls, captions, likes, comments, viewers = fetch_and_process_batch(loader, profile, agenda_start, agenda_end, batch_size)

    # Return the scraped data as a dictionary
    scraped_data = {
        'followers': profile.followers,
        'posts': profile.mediacount,
        'post_urls': post_urls,
        'captions': captions,
        'likes': likes,
        'comments': comments,
        'viewers': viewers,
    }

    return scraped_data