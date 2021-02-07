import csv


def get_info():
    websites = []
    with open('info.csv') as in_file:
        csv_reader = csv.DictReader(in_file)
        for row in csv_reader:
            d = {'url': row["url"], 'retail': row["retail"]}
            websites.append(d)
    return websites
