from datetime import datetime, date
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


def get_content(url, headers, file_name, proxies):
    try:
        if not proxies:
            res = requests.get(url, headers=headers)
        else:
            res = requests.get(url, headers=headers, proxies=proxies)
        if res.status_code != 200:
            append_to_logs(file_name, f"Error, status code: {res.status_code} | {get_time()} | {url}\n")
            while res.status_code == 503:
                append_to_logs(file_name, "Header banned")
                print('generating new header')
                new_header = Headers(os='mac', headers=True).generate()
                get_content(url, new_header, file_name, proxies)
        else:
            return res
    except:
        flag = True
        # if not flag:
        #     print(f"URL not found: {url}")
        #     flag = True
