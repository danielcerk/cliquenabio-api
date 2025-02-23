import re

from bs4 import BeautifulSoup
import requests

def get_favicon(url):

    try:

        page = requests.get(url, timeout=5)
        soup = BeautifulSoup(page.text, 'lxml')

        icon_link = soup.find('link', rel='shortcut icon') or soup.find('link', rel='icon')

        if icon_link and icon_link.has_attr('href'):

            return icon_link['href']

        return url.rstrip('/') + '/favicon.ico'

    except Exception as e:

        print(f"Erro ao buscar favicon: {e}")

        return None

def get_title(url):

    try:

        page = requests.get(url, timeout=5)
        soup = BeautifulSoup(page.text, 'lxml')

        title = soup.find('title')

        return title.string.strip() if title and title.string else None

    except Exception as e:

        print(f"Erro ao buscar título: {e}")

        return None


def get_og_image(url):

    try:

        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'lxml')

        og_image = soup.find('meta', {'property': 'og:image'})

        if og_image and 'content' in og_image.attrs:

            return og_image['content']
        
        else:

            return 'https://online.stl.tech/cdn/shop/products/image_9_80239d75-941f-42bc-b028-9c895b8a7e10.png'

    except Exception as e:

        print(f"Erro ao buscar imagem OG: {e}")

        return None 

def extract_username_and_social_network_of_link(url: str):

    if not isinstance(url, str):

        return 'Entrada inválida', 'Isso não é um link'
    
    try:

        patterns = {

            'Facebook': r'facebook\.com\/(?:profile\.php\?id=)?([^\/?&#]+)\/?(?:\?|#|$)',
            'Instagram': r'instagram\.com\/([^\/?&#]+)\/?(?:\?|#|$)',
            'Twitter': r'x\.com\/([^\/?&#]+)\/?(?:\?|#|$)',
            'LinkedIn': r'linkedin\.com\/in\/([^\/?&#]+)\/?(?:\?|#|$)',
            'TikTok': r'tiktok\.com\/@([^\/?&#]+)\/?(?:\?|#|$)',
            'YouTube': r'youtube\.com\/(?:user|channel)\/([^\/?&#]+)\/?(?:\?|#|$)',
            'Figma': r'figma\.com\/([^\/?&#]+)\/?(?:\?|#|$)',
            'Dribbble': r'dribbble\.com\/([^\/?&#]+)\/?(?:\?|#|$)',
            'Medium': r'medium\.com\/@([^\/?&#]+)\/?(?:\?|#|$)',
            'Behance': r'behance\.net\/([^\/?&#]+)\/?(?:\?|#|$)',
            'Twitch': r'twitch\.tv\/([^\/?&#]+)\/?(?:\?|#|$)',
            'Reddit': r'reddit\.com\/user\/([^\/?&#]+)\/?(?:\?|#|$)',
            'Bluesky': r'bsky\.app\/profile\/([^\/?&#]+)\/?(?:\?|#|$)',
            'GitHub': r'github\.com\/([^\/?&#]+)\/?(?:\?|#|$)',
            'Pinterest': r'pinterest\.com\/([^\/?&#]+)\/?(?:\?|#|$)'
        }


        icon = get_favicon(url)
        og_image = get_og_image(url)
        title = get_title(url)

        for social_network, pattern in patterns.items():

            if not pattern:

                continue

            match = re.search(pattern, url)

            if match:

                username = match.group(1)

                return social_network, username, icon, og_image

        return title, 'Sem usuário', icon, og_image

    except Exception as e:

        return f'O site não existe ou está fora do ar: {e}'
