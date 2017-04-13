import numpy as np
import pandas as pd
import sys

def main():
	csv_path = sys.argv[1]
	in_file = pd.read_csv(csv_path)
	station_file = pd.read_csv('stations.csv')
	birdLat = in_file['LATITUDE']
	birdLon = in_file['LONGITUDE']
	X = station_file['latitude']
	Y = station_file['longitude']
	stations = station_file['ID']
	length = len(birdLat)
	print len(birdLat)
	print len(birdLon)
	nearest_stations = np.chararray(length, itemsize=11)
	for i in range(0, length):
		test_x = birdLat[i].astype(np.float32)
		test_y = birdLon[i].astype(np.float32)
		station_id = find_nearest_neighbor(X, Y, test_x, test_y, stations)
		# in_file['station'][i] = station_id
		nearest_stations[i] = station_id
		# print nearest_stations[i]
	print 'finished finding nearest stations'
	in_file['stations'] = nearest_stations
	out_file = csv_path.split('.')[0] + '_stations.csv'
	in_file.to_csv(out_file, sep=',', encoding='utf-8')


def find_nearest_neighbor(X, Y, x, y, stations):
	X = X.astype(np.float32)
	Y = Y.astype(np.float32)
	dX = X - x
	dY = Y - y
	dX2 = np.square(dX)
	dY2 = np.square(dY)
	square_dist = dX2 + dY2
	nearest = np.argmin(square_dist, axis=0)
	station = stations[nearest]
	return station

if __name__ == "__main__":
	main()

	
