import numpy as np
import pandas as pd
import sys
from datetime import timedelta

def main():

	#This script needs a clusterfinal dataset + a polygon dataset. It merges based on DateTime and fills in the empty cells with 
	#the previous vertices list


	#file naming
	interpolated_data = sys.argv[1]
	polygon_data_with_gaps = sys.argv[2]
	output_file_name = sys.argv[3]


	header1 = [ "LATITUDE", "LONGITUDE", "OBSERVATION COUNT", "temperature", "time_deltas", "OBSERVATION DATE", "COMMON NAME"]
	fields = ['OBSERVATION COUNT']
	header2 = ["AVG LAT", "AVG LON", "COMMON NAME", "OBSERVATION COUNT", "OBSERVATION DATE", "TEMPERATURE", "time_deltas", "VERTICES"]

	df_interpolated = pd.read_csv(interpolated_data, names = header1, skiprows = 1)

	df_poly = pd.read_csv(polygon_data_with_gaps, names = header2,  skiprows = 1)
	df_poly = df_poly[['OBSERVATION DATE', 'VERTICES']]
	df_poly = df_poly.set_index(pd.DatetimeIndex(df_poly['OBSERVATION DATE']))

	#df_interpolated.to_csv(output_file_name)

	merge_poly = pd.merge(df_poly, df_interpolated, how = 'outer', left_index = True, right_index = True)
	merge_poly = merge_poly.drop('OBSERVATION DATE_x', 1)
	merge_poly=merge_poly.rename(columns = {'OBSERVATION DATE_y':'OBSERVATION DATE'})


	bool_list = pd.isnull(merge_poly)
	for i in bool_list.index:	
		if (bool_list.get_value(i, 'VERTICES')):
			prev_poly = merge_poly.get_value(i-pd.DateOffset(days=1), 'VERTICES')
			merge_poly.set_value(i, 'VERTICES', prev_poly)


	merge_poly.to_csv(output_file_name)


if __name__ == "__main__":
	main()