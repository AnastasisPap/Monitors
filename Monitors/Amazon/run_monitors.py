from process_urls import *
from time import sleep
from amazon_scraping import main
import threading


def run_monitors():
    urls = get_urls()
    for url in urls:
        prod_url = url['url']
        price = url['retail']
        thread = threading.Thread(target=main, args=(prod_url, price,))
        thread.start()
        sleep(0.5)


if __name__ == '__main__':
    run_monitors()
