import numpy as np
import pandas as pd
import sys

def main():
	csv_path = sys.argv[1]
	in_file = pd.read_csv(csv_path)
	in_file.drop_duplicates(subset='date_time', inplace=True)

	out_file = csv_path.split('.')[0] + '_nodup.csv'
	in_file.to_csv(out_file, sep=',', encoding='utf-8')

if __name__ == "__main__":
	main() 