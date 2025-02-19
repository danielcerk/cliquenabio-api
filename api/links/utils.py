import re

from bs4 import BeautifulSoup
import requests

def get_favicon(url):

    page = requests.get(url)
    soup = BeautifulSoup(page.text, features="lxml")

    icon_link = soup.find('link', rel='shortcut icon')

    if icon_link is None:

        icon_link = soup.find('link', rel='icon')

    if icon_link is None:

        return url + '/favicon.ico'
    
    return icon_link['href']

def get_title(url):

    page = requests.get(url)
    soup = BeautifulSoup(page.text, features="lxml")

    title = soup.find('title')

    return title.string

def extract_username_and_social_network_of_link(url: str):

    if not isinstance(url, str):

        return 'Entrada inválida', 'Isso não é um link'

    patterns = {

        'Facebook': r'facebook\.com\/(?:profile\.php\?id=)?([^\/?&]+)',
        'Instagram': r'instagram\.com\/([^\/?&]+)',
        'Twitter': r'twitter\.com\/([^\/?&]+)',
        'LinkedIn': r'linkedin\.com\/in\/([^\/?&]+)',
        'TikTok': r'tiktok\.com\/@([^\/?&]+)',
        'YouTube': r'youtube\.com\/(?:user|channel)\/([^\/?&]+)',
        'Figma': r'figma\.com\/([^\/?&]+)',
        'Dribbble': r'dribbble\.com\/([^\/?&]+)',
        'Medium': r'medium\.com\/@([^\/?&]+)',
        'Behance': r'behance\.net\/([^\/?&]+)',
        'Twitch': r'twitch\.tv\/([^\/?&]+)',
        'Reddit': r'reddit\.com\/user\/([^\/?&]+)',
        'Bluesky': r'bsky\.app\/profile\/([^\/?&]+)',
        'GitHub': r'github\.com\/([^\/?&]+)'

    }

    icon = get_favicon(url)
    title = get_title(url)

    for social_network, pattern in patterns.items():

        if not pattern:

            continue

        match = re.search(pattern, url)

        if match:

            username = match.group(1)

            return social_network, username, icon

    return title, 'Sem usuário', icon