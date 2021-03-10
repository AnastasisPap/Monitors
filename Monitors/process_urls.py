import csv
import os


def get_urls(file_name):
    urls = []
    with open(f'../urls/{file_name}') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            urls.append(row)

    return urls


def add_url(file_name, url, price):
    if 'urls' in os.listdir():
        os.chdir('urls')
    with open(f'../urls/{file_name}', 'a', newline='') as file:
        csv_writer = csv.writer(file, delimiter=',')
        csv_writer.writerow([url, price])
