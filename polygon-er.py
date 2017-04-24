import numpy as np
import pandas as pd
import sys

def main():
	csv_path = sys.argv[1]
	in_file = pd.read_csv(csv_path)
	dates = in_file['OBSERVATION DATE']
	lats = in_file['LATITUDE']
	lons = in_file['LONGITUDE']
	name = in_file['COMMON NAME']
	count = in_file['OBSERVATION COUNT']
	t_deltas = in_file['time_deltas']
	temps = in_file['temperature']

	length = len(dates)
	i = 0
	xSum = 0
	ySum = 0
	dupCount = 1

	rows_list = []

	# each row
	while(i < length - 1):
		row_dict = {}
		xSum = lats[i]
		ySum = lons[i]
		obsCount = count[i]
		the_date = dates[i]
		the_temp = temps[i]
		the_delta = t_deltas[i]

		# this is local to a given day. needs to be added to something that will resemble a column in the dataframe
		vertices = ["%.2f*%.2f" % (lats[i], lons[i])]

		while(dates[i + 1] == dates[i]):
			xSum += lats[i + 1]
			ySum += lons[i + 1]
			obsCount += count[i + 1]
			dupCount += 1
			vertices.append("%.2f*%.2f*%d" % (lats[i + 1], lons[i + 1], count[i + 1]))
			i += 1

		xAvg = xSum / float(dupCount)
		yAvg = ySum / float(dupCount)
		row_dict['OBSERVATION_DATE'] = dates[i]
		row_dict['COMMON NAME'] = name[i]
		row_dict['AVG LAT'] = xAvg
		row_dict['AVG LON'] = yAvg
		row_dict['OBSERVATION COUNT'] = obsCount
		row_dict['TIME_DELTAS'] = the_delta
		row_dict['TEMPERATURE'] = the_temp
		row_dict['VERTICES'] = '&'.join(vertices) # 2.4*5.2&3.5*2.1 == [(2.4, 5,2), (3.5, 2.1)]
		dupCount = 1

		rows_list.append(row_dict)
		i += 1 #iterate

	out_df = pd.DataFrame(rows_list)
	out_file = csv_path.split('.')[0] + '_poly.csv'
	out_df.to_csv(out_file, sep=',', encoding='utf-8')

if __name__ == "__main__":
	main()
