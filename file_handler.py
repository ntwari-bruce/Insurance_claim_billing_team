import csv
import os

# we are parsing the csv file and returning a list of dictionaries
def load_csv(file_path):
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        return list(reader)
