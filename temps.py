import numpy as np
import pandas as pd
import sys
import itertools
import csv

def main():

	with open('ghcnd-stations.txt', 'r') as in_file:
		for line in in_file:
			print line[0:12]


if __name__ == "__main__":
	main()