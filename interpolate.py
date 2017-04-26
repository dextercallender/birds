import numpy as np
import pandas as pd
import sys

def main():

	input_file_name = sys.argv[1]
	#pass in what you want the new name to be

	output_file_name = input_file_name.split('.')[0] + 'final.csv'

	header = ["COMMON NAME", "LATITUDE", "LONGITUDE", "OBSERVATION COUNT","OBSERVATION DATE", "temperature", "time_deltas"]
	df = pd.read_csv(input_file_name, names = header, skiprows = 1)
	common_name = df.get_value(1, 'COMMON NAME')

	#change OBSERVATION DATE to date-time-index
	df['DATETIME'] = pd.to_datetime(df['OBSERVATION DATE'])

	#df['DATETIME'] = pd.DatetimeIndex(df['OBSERVATION DATE'])
	df = df.set_index(pd.DatetimeIndex(df['DATETIME']))
	

	df = df.resample('D').mean()
	df = df.interpolate(method = 'time')

	df['OBSERVATION_DATETIME'] = df.index
	#readd common name column
	df['COMMON NAME'] = common_name

	df.to_csv(output_file_name)

if __name__ == "__main__":
	main()