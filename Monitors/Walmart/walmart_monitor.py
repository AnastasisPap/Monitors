from bs4 import BeautifulSoup
from send_webhook import send_webhook
from time import sleep
from global_functions import *
file_name = 'walmart_logs.txt'


def check_availability(soup):
    try:
        availability_div = soup.find('div', class_='prod-blitz-copy-message').text
        if "out of stock" in availability_div:
            return False
        return True
    except:
        return True


def get_title(soup):
    try:
        title = soup.find('h1', {'itemprop': 'name'}).text
        return title
    except:
        append_to_logs(file_name, f'Error finding title {get_time()}\n')


def get_image_url(soup):
    try:
        image_div = soup.find('div', class_='hover-zoom-hero-image-container').find('img')
        image_url = 'https:' + image_div["src"]
        return image_url
    except:
        append_to_logs(file_name, f'Error finding image url {get_time()}')
        return 'https://developers.google.com/maps/documentation/streetview/images/error-image-generic.png'


def get_price(soup):
    try:
        price_span = soup.find('span', class_='price-characteristic')["content"]
        return '$' + price_span
    except:
        append_to_logs(file_name, f'Error finding price {get_time()}\n')


def main(url):
    hasSent = False
    append_to_logs(file_name, f'Started monitor {get_time()}\n')

    while True:
        res = get_content(url, file_name, None)
        if res:
            soup = BeautifulSoup(res.content, 'html.parser')
            isAvailable = check_availability(soup)
            if not isAvailable and hasSent:
                hasSent = False

            print(soup.prettify())
            if isAvailable and not hasSent:
                title = get_title(soup)
                price = get_price(soup)
                image_url = get_image_url(soup)
                product_id = url.split('/')[-1]
                send_webhook(url, 'Walmart: item in stock', title, image_url, price, product_id)
                hasSent = True
        sleep(2)


if __name__ == "__main__":
    _url = 'https://www.walmart.com/ip/PlayStation-5-Console/363472942'
    main('https://www.walmart.com/ip/VIZIO-50-Class-4K-UHD-LED-SmartCast-Smart-TV-V-Series-V505-G-H/449340109')
