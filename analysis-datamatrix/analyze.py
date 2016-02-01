#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from analysis import parse, pupil

dm = parse.parsefolder('../data', cacheid='data')
dm = pupil.preprocess(dm)
pupil.plot_pupiltrace(dm)
