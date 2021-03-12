from datetime import datetime
import requests
from fake_headers import Headers
import os


def append_to_logs(file_name, message):
    if 'logs' not in os.listdir():
        os.mkdir('logs')
    file_path = "./logs/" + file_name
    with open(file_path, 'a') as logs:
        logs.write(message)


def get_time():
    return f'{str(datetime.now())}'


def get_proxy(_proxy):
    with open('../proxies.txt', 'r') as file:
        lines = file.readlines()

    proxies = []
    for line in lines:
        proxy = line.strip('\n').split(':')
        formatted_proxy = f'http://{proxy[2]}:{proxy[3]}@{proxy[0]}:{proxy[1]}'
        proxies.append(formatted_proxy)

    if _proxy not in proxies:
        return proxies[0]
    idx = proxies.index(_proxy)
    if idx + 1 < len(proxies):
        return proxies[idx+1]
    return None


def get_content(url, file_name, proxies):
    try:
        headers = Headers(os='win', headers=True).generate()

        if not proxies:
            res = requests.get(url, headers=headers)
        else:
            res = requests.get(url, headers=headers, proxies=proxies)

        if res.status_code != 200:
            append_to_logs(file_name, f"Error, status code: {res.status_code} | {get_time()} | {url}\n")
            if res.status_code == 403:
                print('Banned')
                proxy = get_proxy(proxies)
                if proxy:
                    get_content(url, file_name, proxy)
                else:
                    return None
        else:
            return res
    except:
        flag = True
        # if not flag:
        #     print(f"URL not found: {url}")
        #     flag = True
