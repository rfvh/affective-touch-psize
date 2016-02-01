#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import numpy as np
from datamatrix import io, DataMatrix, SeriesColumn, cached

def parsefile(path):

	"""
	desc:
		Parse a single .txt data file, and return it as a DataMatrix.

	arguments:
		path:
			desc:	The path to the data file.
			type:	str

	returns:
		type:	DataMatrix
	"""

	print('Reading %s' % path)
	src = io.readtxt(path, delimiter='\t')
	dm = DataMatrix(length=0)
	trialdm = None
	for row in src:
		if isinstance(row.state, str):
			if 'start_trial' in row.state:
				if trialdm is not None:
					print('%d: %d samples (%d invalid) %s' \
						% (trialdm.trialid[0], sample, invalid, \
						trialdm.snelheid[0]))
					dm <<= trialdm
				trialdm = DataMatrix(length=1)
				trialdm.pupil = SeriesColumn(1000)
				trialdm.trialid = int(row.state.split()[1])
				trialdm.path = path
				sample = 0
				invalid = 0
				continue
			if 'var' in row.state:
				l = row.state[4:].split(maxsplit=1)
				if len(l) == 1:
					continue
				var, val = tuple(l)
				# Length is a special property for datamatrix
				if var == 'length':
					var = '_length'
				trialdm[var] = val
				continue
			continue
		if trialdm is not None:
			if row.Rpsize != '' and row.Rpsize > 0:
				trialdm.pupil[0, sample] = row.Rpsize
			else:
				trialdm.pupil[0, sample] = np.nan
				invalid += 1
			sample += 1
	dm <<= trialdm
	return dm


@cached
def parsefolder(folder):

	"""
	desc:
		Parse a folder full of .txt data files, and returns this as a
		DataMatrix.

	arguments:
		folder:
			desc:	Folder path
			type:	str

	returns:
		type:	DataMatrix
	"""

	dm = DataMatrix(length=0)
	for path in os.listdir(folder):
		if path.startswith('.'):
			continue
		dm <<= parsefile(os.path.join(folder, path))
	return dm
