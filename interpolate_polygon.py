import numpy as np
import pandas as pd
import sys
from datetime import timedelta

def main():

	
	interpolated_data = sys.argv[1]
	polygon_data_with_gaps = sys.argv[2]
	output_file_name = sys.argv[3]


	header1 = ["COMMON NAME", "LATITUDE", "LONGITUDE", "OBSERVATION COUNT","OBSERVATION DATE", "temperature", "time_deltas"]
	fields = ['OBSERVATION COUNT']
	header2 = ["AVG LAT", "AVG LON", "COMMON NAME", "OBSERVATION COUNT", "OBSERVATION DATE", "TEMPERATURE", "time_deltas", "VERTICES"]

	df_interpolated = pd.read_csv(interpolated_data, names = header1, skiprows = 1)

	df_poly = pd.read_csv(polygon_data_with_gaps, names = header2,  skiprows = 1)
	df_poly = df_poly[['OBSERVATION DATE', 'VERTICES']]

	df_poly = df_poly.set_index(pd.DatetimeIndex(df_poly['OBSERVATION DATE']))

	merge_poly = pd.merge(df_poly, df_interpolated, how = 'outer', left_index = True, right_index = True)

	merge_poly = merge_poly.drop('OBSERVATION DATE_x', 1)

	bool_list = pd.isnull(merge_poly)
	#print(bool_list)

	

	for i in bool_list.index:
		
		if (bool_list.get_value(i, 'VERTICES')):
			prev_poly = merge_poly.get_value(i-pd.DateOffset(days=1), 'VERTICES')
			merge_poly.set_value(i, 'VERTICES', prev_poly)











	merge_poly.to_csv(output_file_name)


if __name__ == "__main__":
	main()