import numpy as np
import pandas as pd
import sys
from datetime import datetime

def main():
	csv_path = sys.argv[1]

	input_data = pd.read_csv(csv_path)
	input_data['TIME OBSERVATIONS STARTED'].fillna('00:00:00')

	# represent observations without a count as a 'unit' observation
	input_data['OBSERVATION COUNT'].replace(to_replace='X', value=1, inplace=True)

	input_data['date_time'] = input_data['OBSERVATION DATE'] + ' ' + input_data['TIME OBSERVATIONS STARTED']
	# 'datetime' column format looks like this: 2011-01-01 00:00:00
	input_data['date_time'] = pd.to_datetime(input_data['date_time'], format='%Y-%m-%d %H:%M:%S') #creates array of timestamp objects
	input_data.index = input_data['date_time']
	input_data = input_data.sort_index()
	
	# time_deltas are generated specific to this project, which only uses data between Jan 1st, 2011 and Jan 1st, 2016
	time_deltas = input_data['date_time'] - datetime(2011,1,1) # create Panda Timedelta types

	input_data['time_deltas'] = time_deltas.astype('timedelta64[s]')

	print input_data['time_deltas'][0:20]

	drop_cols = [0,1,2,3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16 ,17, 18, 19, 20, 21, 22,23,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47]
	input_data.drop(input_data.columns[drop_cols], axis=1, inplace=True)
	outfile = csv_path.split('.')[0] + '_pr.csv'
	input_data.to_csv(outfile, sep=',', encoding='utf-8')



if __name__ == "__main__":
	main()





