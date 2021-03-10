import csv
import os


def get_urls():
    urls = []
    with open('../urls/amazon_urls.csv') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            urls.append(row)

    return urls


def add_url(url, price):
    if 'urls' in os.listdir():
        os.chdir('urls')
    with open('../urls/amazon_urls.csv', 'a', newline='') as file:
        csv_writer = csv.writer(file, delimiter=',')
        csv_writer.writerow([url, price])

    os.chdir('../Amazon')
