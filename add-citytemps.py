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
	date_col = in_file['OBSERVATION_DATETIME']
	lat_col = in_file['LATITUDE']
	lon_col = in_file['LONGITUDE']
	length = len(date_col)
	print 'length' + str(length)

	df = pd.DataFrame(index=date_col)

	city_coords = {}
	city_coords['reykjavik'] = (64.13, -21.81)
	city_coords['vancouver'] = (49.28, -123.12)
	city_coords['anchorage'] = (61.21, -149.9)
	city_coords['nyc'] = (40.7, -74.0)
	city_coords['albuquerque'] = (35.08, -106.60)
	city_coords['mexico_city'] = (19.43, -99.13)
	city_coords['brasilia'] = (-15.79, -47.88)
	city_coords['buenos_aires'] = (-34.60, -58.38)
	city_coords['cape_horn'] = (-54.93, -67.61)

	city_temps = {}
	city_temps['reykjavik'] = np.empty(length)
	city_temps['vancouver'] = np.empty(length)
	city_temps['anchorage'] = np.empty(length)
	city_temps['nyc'] = np.empty(length)
	city_temps['albuquerque'] = np.empty(length)
	city_temps['mexico_city'] = np.empty(length)
	city_temps['brasilia'] = np.empty(length)
	city_temps['buenos_aires'] = np.empty(length)
	city_temps['cape_horn'] = np.empty(length)


	# print temps.shape
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

		for city in city_coords:
			lat = round_pt5(city_coords[city][0])
			lon = round_pt5(city_coords[city][1])

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
			city_temps[city][i] = temp

	for city in city_temps:
		df[city] = city_temps[city]

	out_file = 'city_temps.csv'
	df.to_csv(out_file, sep=',', encoding='utf-8')

if __name__ == "__main__":
	main()