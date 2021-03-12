from process_urls import *
from time import sleep
from gamestop_monitor import main
import threading


def run_monitors():
    urls = get_urls('gamestop_urls.csv')
    for url in urls:
        prod_url = url['url']
        thread = threading.Thread(target=main, args=(prod_url,))
        thread.start()
        sleep(0.5)


if __name__ == '__main__':
    run_monitors()
