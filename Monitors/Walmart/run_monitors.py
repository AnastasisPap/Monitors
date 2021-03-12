from process_urls import *
from time import sleep
from walmart_monitor import main
import threading


def run_monitor():
    urls = get_urls('walmart_urls.csv')

    for url in urls:
        prod_url = url['url']
        thread = threading.Thread(target=main, args=(prod_url,))
        thread.start()
        sleep(0.5)


if __name__ == '__main__':
    run_monitor()
