from bs4 import BeautifulSoup
from read_csv import get_info
from send_webhook import send_webhook
from time import sleep
from global_functions import *
file_name = 'very_logs.txt'


def check_availability(soup):
    try:
        oos_text = soup.find('meta', {'property': 'product:availability'})["content"]
        if oos_text == 'Out of stock':
            return False
        return True
    except:
        append_to_logs(file_name, f'Error finding availability {get_time()}\n')
        append_to_logs(file_name, f'{soup.prettify()}')


def get_price(soup):
    try:
        price = soup.find('meta', {'property': 'product:price:amount'})["content"]
        return '£' + price
    except:
        append_to_logs(file_name, f'Error finding price {get_time()}\n')
        append_to_logs(file_name, f'{soup.prettify()}')


def get_url(soup):
    try:
        url = soup.find('meta', {'property': 'og:url'})
        return url
    except:
        append_to_logs(file_name, f'Error finding url {get_time()}\n')
        append_to_logs(file_name, f'{soup.prettify()}')


def get_title_image_url(soup):
    try:
        image_div = soup.find(id='amp-originalImage').find('img')
        image_url = image_div["src"]
        title = image_div["title"].split("-")
        title = ' '.join(title)
        return title, image_url
    except:
        append_to_logs(file_name, f'Error finding image url {get_time()}\n')
        append_to_logs(file_name, f'{soup.prettify()}')


def main(url):
    hasSent = False

    append_to_logs(file_name, f'Started monitor {get_time()}\n')
    while True:
        headers = {'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36', 'Accept-Language': 'en-US;q=0.5,en;q=0.3', 'Cache-Control': 'max-age=0', 'DNT': '1', 'Pragma': 'no-cache'}
        res = get_content(url, headers, file_name)
        
        if res:
            soup = BeautifulSoup(res.content, 'html.parser')
            isAvailable = check_availability(soup)
            if not isAvailable and hasSent:
                hasSent = False

            if isAvailable and not hasSent:
                title, image_url = get_title_image_url(soup)
                price = get_price(soup)
                product_id = url.split('/')[-1].strip('.prd')
                send_webhook(url, "Very: item in stock", title, image_url, price, product_id)

        sleep(2)


if __name__ == '__main__':
    websites = get_info()[0]
    _url = websites['very_url']
    main(_url)
