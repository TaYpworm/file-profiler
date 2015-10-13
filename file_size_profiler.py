#!/usr/bin/python

import json
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from optparse import OptionParser
import os

def main():
	parser = OptionParser()
	parser.add_option('-d', '--directory', dest='dir', action='store', help='top-level directory to profile')

	option, args = parser.parse_args()

	file_sizes = get_file_sizes(option.dir)
	hist, edges = bin_files_by_transact_size(file_sizes)
	print json.dumps({ 'hist': hist.tolist(),
			'edges': edges.tolist()
		})

def get_file_sizes(dir):
	file_sizes = []
	for tld_name, dir_names, file_names in os.walk(dir):
		for dir_name in dir_names:
			file_sizes.extend(get_file_sizes(os.path.join(tld_name, dir_name)))
		for file_name in file_names:
			file_sizes.append(os.stat(os.path.join(tld_name, file_name)).st_size)

	return file_sizes

def bin_files_by_transact_size(file_sizes):
	mb_scalar = 1024.0 ** 2
	bins = [2**x / mb_scalar for x in range(1, 48)]
	return np.histogram(map(lambda x: x / mb_scalar, file_sizes), bins)

if __name__ == '__main__':
	main()