# -*- coding: utf-8 -*-

from matplotlib import pyplot as plt
from datamatrix import plot, series
from datamatrix.rbridge import lme4
from datamatrix.colors.tango import *
import numpy as np

def preprocess_exp2(dm):

	"""
	desc:
		Do basic data preprocessing that is specific to experiment 2.

	arguments:
		dm:
			type: DataMatrix

	returns:
		type:	DataMatrix
	"""

	# Snelheid and storking side were incorrectly coded. The order was fixed, so
	# here we recode it manually.
	dm.snelheid = 345 * [3, 30, 0.3, 30, 3, 0.3]
	dm.side = 345 * ['V', 'D', 'D', 'V', 'D', 'V']
	for row in dm:
		row.subject_nr = int(str(row.subject_nr)[:-1])
	return dm


def preprocess(dm):

	"""
	desc:
		Do basic data preprocessing.

	arguments:
		dm:
			type: DataMatrix

	returns:
		type:	DataMatrix
	"""

	dm.pupil.depth = 540
	dm.pupil = series.baseline(dm.pupil, baseline=dm.pupil, bl_start=50,
		bl_end=90)
	dm.pupil = series.smooth(dm.pupil, winlen=11)
	dm.rename('snelheid', 'velocity')
	dm.log_velocity = np.log10(dm.velocity)
	return dm


def plot_pupiltrace(dm, suffix='', interaction=False):

	"""
	desc:
		Create a plot of the pupil trace annotated with significant regions.

	arguments:
		dm:
			type: DataMatrix

	keywords:
		suffix:			A suffix for the plot.
		interaction:	Indicates whether the log_velocity by side interaction
						should be included.
	"""

	plot.new(size=(12, 6))
	# Plot the three velocities as separate lines
	for color, velocity in ( (orange[1], 30), (blue[1], 3), (green[1], .3) ):
		dm_ = dm.velocity == velocity
		plot.trace(dm_.pupil, label='%s cm/s (N=%d)' % (velocity, len(dm_)),
			color=color)
	# Run statistical model, and annotate the figure with three alpha levels:
	# .05, .01, and .005
	if interaction:
		model = 'pupil ~ log_velocity*side + (1+log_velocity*side|subject_nr)'
	else:
		model = 'pupil ~ log_velocity + (1+log_velocity|subject_nr)'
	lm = lme4.lmer_series(dm, formula=model, winlen=3,
		cacheid='lmer%s' % suffix)
	for y, color1, color2, alpha in [
		(.94, grey[2], blue[0], .05),
		(.942, grey[3], blue[1], .01),
		(.944, grey[4], blue[2], .005),
		(.946, grey[5], blue[2], .001)
		]:
		a = series.threshold(lm.p, lambda p: p > 0 and p < alpha,
			min_length=1)
		plot.threshold(a[1], y=y, color=color1, linewidth=4)
		if interaction:
			plot.threshold(a[3], y=y+.01, color=color2, linewidth=4)
	# Mark the baseline period
	plt.axvspan(50, 90, color='black', alpha=.2)
	# Mark the cue onset
	plt.axvline(90, color='black')
	# Adjust the x axis such that 0 is the cue onset, and the units are time in
	# seconds (assuming 33 ms per sample)
	plt.xticks(np.arange(40, 540, 50), np.arange(-50, 450, 50)*.033)
	plt.xlim(0, 540)
	plt.xlabel('Time since auditory cue (s)')
	plt.ylabel('Pupil size (relative to baseline)')
	plt.legend(frameon=False)
	plot.save('pupiltrace'+suffix)
