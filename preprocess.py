import numpy as np
import pandas as pd

from datetime import datetime

def main():
	csv_path = sys.argv[1]
	# raw_data = csv.reader(open(csv_path), delimiter=',')
	# timesorted_data = sorted(raw_data, key = lambda row: operator.itemgetter(0)) # index here refers to column number
	FORMAT_STRING = 'SOMETHING'
	dateparser = lambda x: pd.datetime.strptime(x, FORMAT_STRING)
	raw = pd.read_csv(csv_path, parse_dates = {'datetime': ['OBSERVATION DATE', 'TIME OBSERVATIONS STARTED']}, date_parser=dateparser)
	raw.index = raw['datetime']
	date_sorted = raw.sort_index()
	print date_sorted['datetime'][10]





