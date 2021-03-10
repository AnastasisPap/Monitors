from process_urls import *
from time import sleep
from currys_monitor import main
import threading


def run_monitors():
    urls = get_urls('currys_urls.csv')
    for url in urls:
        prod_url = url['url']
        keyword = url['keyword']
        thread = threading.Thread(target=main, args=(prod_url, keyword,))
        thread.start()
        sleep(0.5)


if __name__ == '__main__':
    run_monitors()
