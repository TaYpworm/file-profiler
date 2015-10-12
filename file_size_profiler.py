#!/usr/bin/python

import json
import matplotlib.pyplot as plt
import numpy as np
from optparse import OptionParser
import os

def main():
	parser = OptionParser()
	parser.add_option('-d', '--directory', dest='dir', action='store', help='top-level directory to profile')
	parser.add_option('-p', '--plot', dest='plot', action='store', default='file_size_histgram.png', help='file to write histogram')

	option, args = parser.parse_args()

	file_sizes = get_file_sizes(option.dir)
	hist, edges = bin_files_by_transact_size(file_sizes)
	plot_to_file(option.plot, hist, edges)

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
	bins = [2**x / mb_scalar for x in range(12, 50)]
	return np.histogram(map(lambda x: x / mb_scalar, file_sizes), bins)

def plot_to_file(file_name, hist, edges):
	plt.bar(edges[:-1], hist, edgecolor='red')
	#plt.xlim(min(edges), max(edges))
	plt.savefig(file_name)

if __name__ == '__main__':
	main()