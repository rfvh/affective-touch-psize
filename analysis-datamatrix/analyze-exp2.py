#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from analysis import parse, pupil

dm = parse.parsefolder('../data-exp2', cacheid='data-exp2')
dm = pupil.preprocess_exp2(dm)
dm = pupil.preprocess(dm)
pupil.plot_pupiltrace(dm, '-exp2', interaction=True)
pupil.plot_pupiltrace(dm.side == 'V', '-exp2-ventral')
pupil.plot_pupiltrace(dm.side == 'D', '-exp2-dorsal')
