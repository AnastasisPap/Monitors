import requests
from bs4 import BeautifulSoup
from read_csv import get_info
from send_webhook import send_webhook
from time import sleep
from fake_headers import Headers
from write_to_logs import append_to_logs


def get_headers():
    return Headers(os="mac", headers=True).generate()


def get_content(url, headers):
    try:
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            append_to_logs(f"Error, status code: {status_code}\n")
            print(f"Got status code: {res.status_code}")
            while res.status_code == 503:
                print("Header banned")
                get_content(url, get_headers())
        else:
            return res
    except:
        print(f"URL not found: {url}")


def get_product_title(soup):
    try:
        title = soup.find(id='productTitle')
        return title.text.strip('\n')
    except:
        append_to_logs("Error finding product title html code:\n")
        append_to_logs(soup.prettify())


def check_availability(soup):
    try:
        available = soup.find(id='availability')
        try:
           available_text = available.find('span', class_="a-size-medium").contents[0].lower()
           kws = ["no disponible", "unavailable", "nicht"]
            or kw in kws:
                f kw in available_text:
                    eturn False
           return True
       except:
           append_to_logs("Error finding availability text, script:\n")
           append_to_logs(available.prettify())
    except:
        append_to_logs("Error finding availability, script:\n")
        append_to_logs(soup.prettify())


def get_image_url(soup):
    try:
        main_product = soup.find('li',a class_='itemNo0')
        image = main_product.find('img')
        url = image['data-old-hires']
        return url
    except:
        append_to_logs("Error finding image, script:\n")
        append_to_logs(soup.prettify())


def main(url):
    while True:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15'}
        res = get_content(url, headers)
        if res:
            soup = BeautifulSoup(res.content, 'html.parser')
            isAvailable = check_availability(soup)
            productTitle = get_product_title(soup)
            append_to_logs("Checking availability\n")
            if isAvailable:
                image_url = get_image_url(soup)
                send_webhook(url, 'Item in stock', productTitle, image_url)
        sleep(3)


if __name__ == '__main__':
    websites = get_info()
    main(websites[0]['url'])

