import csv

def get_info():
    websites = []
    with open('info.csv') as in_file:
        csv_reader = csv.DictReader(in_file)
        for row in csv_reader:
            d = {'website': row["website"], 'url': row["url"], 'class_to_search': row["class_to_search"].split(';'), 'id': row['id'].split(';')}
            websites.append(d)
    return websites
