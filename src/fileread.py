import csv

def get_csv_reader(path):
    with open(path, 'rb') as infile:
        reader = csv.reader(infile)
        for row in reader:
            yield row
