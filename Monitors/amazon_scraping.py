import requests
from bs4 import BeautifulSoup
from read_csv import get_info
from send_webhook import send_webhook
from time import sleep


def get_content(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15'}
    try:
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            print(f"Got status code: {res.status_code}")
        else:
            return res
    except:
        print(f"URL not found: {url}")


def get_product_title(soup):
    title = soup.find(id='productTitle')
    return title.text.strip('\n')


def check_availability(soup):
    available = soup.find(id='availability')
    available_text = available.find('span', class_="a-size-medium").contents[0].lower()
    if "in stock" in available_text:
        return True
    return False


def get_image_url(soup):
    main_product = soup.find('li', class_='itemNo0')
    image = main_product.find('img')
    url = image['data-old-hires']
    return url


def main():
    websites = get_info()
    for website in websites:
        url = website['url']
        res = get_content(url)
        if res:
            soup = BeautifulSoup(res.content, 'html.parser')
            isAvailable = check_availability(soup)
            productTitle = get_product_title(soup)
            if isAvailable:
                image_url = get_image_url(soup)
                send_webhook(url, 'Item in stock', productTitle, image_url)


if __name__ == '__main__':
    main()

