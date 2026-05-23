import csv

from config.config_reader import config


def get_search_data(row_name):
    with open(config.search_data_file, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if row["row_name"] == row_name:
                return row

    raise ValueError(f"No test data row found for: {row_name}")

