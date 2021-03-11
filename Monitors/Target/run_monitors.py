from process_urls import *
from time import sleep
from target_monitor import *
import threading


def run_monitors():
    ids = get_urls('target_urls.csv')
    for item in ids:
        prod_id = item['id']
        thread = threading.Thread(target=main, args=(prod_id,))
        thread.start()
        sleep(0.5)


if __name__ == '__main__':
    run_monitors()
