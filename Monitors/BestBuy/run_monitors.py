from process_urls import *
from time import sleep
from best_buy_monitor import main
import threading


def run_monitors():
    ids = get_urls('best_buy_ids.csv')
    for prod_id in ids:
        prod_id = prod_id['id']
        thread = threading.Thread(target=main, args=(prod_id,))
        thread.start()
        sleep(0.5)


if __name__ == '__main__':
    run_monitors()