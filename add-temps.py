from netCDF4 import Dataset
import numpy as np
import pandas as pd
import sys

t2011 = Dataset("air.sig995.2011.nc", "r")
t2012 = Dataset("air.sig995.2012.nc", "r")
t2013 = Dataset("air.sig995.2013.nc", "r")
t2014 = Dataset("air.sig995.2014.nc", "r")
t2015 = Dataset("air.sig995.2015.nc", "r")
t2016 = Dataset("air.sig995.2016.nc", "r")
air_2011 = t2011['air'][:]
air_2012= t2012['air'][:]
air_2013 = t2013['air'][:]
air_2014 = t2014['air'][:]
air_2015 = t2015['air'][:]
air_2016 = t2016['air'][:]

print air_2011.shape
print air_2012.shape
print air_2013.shape
print air_2014.shape
print air_2015.shape
print air_2016.shape


air_year_dict = {'2011': air_2011, '2012': air_2012, '2013': air_2013, '2014': air_2014, '2015': air_2015, '2016': air_2016}

def get_days(month, day):
	month2day = {'01': 0,'02': 31, '03': 59, '04': 90, '05': 120, '06': 151, '07': 181, '08': 212, '09': 243, '10': 273, '11': 304, '12': 334}
	return month2day[month] + int(day)

def round_pt5(coord):
	return round(coord * 2) / 2

def sad():
	print get_days('09', '17')
	print get_days('03', '03')

def main():
	csv_path = sys.argv[1]
	in_file = pd.read_csv(csv_path)
	date_col = in_file['OBSERVATION DATE']
	lat_col = in_file['LATITUDE']
	lon_col = in_file['LONGITUDE']
	length = len(date_col)
	print 'length' + str(length)

	temps = np.empty(length)
	print temps.shape
	print 'getting temperatures for ' + csv_path.split('/')[1]
	for i in range(len(date_col)):
		has_365 = 0

		date = date_col[i].split('-')
		year = date[0]
		month = date[1]
		day = date[2]
		nth_day = get_days(month, day)

		cdf = air_year_dict[year]
		# some netCDF4 sets have a time axis of len 365, some 366!! Wtf!!!
		if cdf.shape[0] == 365:
			has_365 = 1

		lat = round_pt5(float(lat_col[i]))
		lon = round_pt5(float(lon_col[i]))

		# go from [-180, 180] --> [0, 360]
		if lon < 0:
			lon = lon + 360.0

		lon_idx = int((lon / 360.0) * 144.0)
		lat_idx = int(((lat - 90) / -180.0) * 73.0)
		# one edge case where the nearest int operation won't index the array properly
		if lat_idx == 73:
			lat_idx = 72

		if nth_day == 365 and has_365 == 1:
			nth_day = 364 #this is horrible

		temp = cdf[nth_day, lat_idx, lon_idx]
		temps[i] = temp

	in_file['temperature'] = temps
	out_file = csv_path.split('.')[0] + '_temps.csv'
	in_file.to_csv(out_file, sep=',', encoding='utf-8')

if __name__ == "__main__":
	main()
