import csv
from io import TextIOWrapper

def stream_csv_rows(path):
    with open(path, "rb") as f:
        wrapper = TextIOWrapper(f, encoding="utf-8", errors="ignore")
        reader = csv.DictReader(wrapper)
        for r in reader:
            yield r
