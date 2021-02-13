import requests
from datetime import datetime
from bs4 import BeautifulSoup
import re
import json


def login(username, password):
    link = 'https://www.instagram.com/accounts/login/'
    login_url = 'https://www.instagram.com/accounts/login/ajax/'

    time = int(datetime.now().timestamp())
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    res = requests.get(link, headers=headers)
    soup = BeautifulSoup(res.content, 'html.parser')
    pattern = re.compile(r"window._sharedData = \{(.*?)\}")
    new_soup = soup.find('script', text=pattern)
    csrf_token = str(new_soup).split("{")[2].split(',')[0].split(':')[1][1:][:-1]

    payload = {
        'username': username,
        'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:{password}',
        'queryParams': {},
        'optIntoOneTap': 'false'
    }

    login_header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.instagram.com/accounts/login/",
        "x-csrftoken": csrf_token
    }

    login_response = requests.post(login_url, data=payload, headers=login_header)
    json_data = json.loads(login_response.text)

    if json_data["authenticated"]:
        print("Login successful")
        cookies = login_response.cookies
        cookie_jar = cookies.get_dict()
        csrf_token = cookie_jar['csrftoken']
        session_id = cookie_jar['sessionid']
        return csrf_token, session_id
    else:
        print("Login failed ", login_response.text)
        return None, None
