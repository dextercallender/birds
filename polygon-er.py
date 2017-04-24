import numpy as np
import pandas as pd
import sys

def main():
	csv_path = sys.argv[1]
	in_file = pd.read_csv(csv_path)
	dates = in_file['OBSERVATION DATE']
	lats = in_file['AVG LAT']
	lons = in_file['AVG LON']
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
		vertices = ["%.2f*%.2f" % (lats[i], lons[j])]

		while(dates[i + 1] == dates[i]):
			j = i
			xSum += lats[i + 1]
			ySum += lons[i + 1]
			obsCount += count[i + 1]
			dupCount += 1
			vertices.append("%.2f*%.2f" % (lats[i + 1], lons[j + 1]))
			i += 1

		xAvg = xSum / float(dupCount)
		yAvg = ySum / float(dupCount)
		row_dict['OBSERVATION_DATE'] = dates[i]
		row_dict['COMMON NAME'] = name[i]
		row_dict['LATITUDE'] = xAvg
		row_dict['LONGITUDE'] = yAvg
		row_dict['OBSERVATION COUNT'] = obsCount
		row_dict['time_deltas'] = the_delta
		row_dict['temperature'] = the_temp
		row_dict['vertices'] = '&'.join(vertices) # 2.4*5.2&3.5*2.1 == [(2.4, 5,2), (3.5, 2.1)]
		dupCount = 1

		rows_list.append(row_dict)
		i += 1 #iterate

	out_df = pd.DataFrame(rows_list)
	out_file = csv_path.split('.')[0] + '_clustered.csv'
	out_df.to_csv(out_file, sep=',', encoding='utf-8')

if __name__ == "__main__":
	main()
