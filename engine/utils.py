import csv


def load_csv(path):
    with open(path, newline='\n', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)
