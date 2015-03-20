#!/usr/bin/env python

"""
Created on 2015-03-19T16:19:41
"""

from __future__ import division, print_function
import sys
from pyutil.pyutil import wgtdMean as wm

try:
    import numpy as np
except ImportError:
    print('You need numpy installed')
    sys.exit(1)

try:
    import pandas as pd
except ImportError:
    print('You need pandas installed')
    sys.exit(1)

__author__ = "Matt Giguere (github: @mattgiguere)"
__maintainer__ = "Matt Giguere"
__email__ = "matthew.giguere@yale.edu"
__status__ = " Development NOT(Prototype or Production)"
__version__ = '0.0.1'


def test_getNewTimes_one_day_bin_ten_days():
    """
    Test to make sure `getNewTimes` returns ten elements
    when 75 elements are entered over a ten day span with
    one day binning in place.
    """
    times = np.random.uniform(0, 10, 75)
    newtimes = wm.getNewTimes(times, 1.)
    print(len(newtimes))
    assert len(newtimes) == 10


def test_getNewTimes_with_half_phase_one_day_bin():
    """
    Test to make sure times are shifted
    properly if the phase optional argument
    is used.
    """
    times = np.random.uniform(0, 10, 75)
    newtimes = wm.getNewTimes(times, 1.)
    newtimes2 = wm.getNewTimes(times, 1., phase=0.5)
    assert np.round((np.min(newtimes2) - np.min(newtimes)), 7) == 0.5


def test_getNewTimes_with_half_phase_two_day_bin():
    """
    Test to make sure times are shifted
    properly if the phase optional argument
    is used with a two day bin.
    """
    times = np.random.uniform(0, 10, 75)
    newtimes = wm.getNewTimes(times, 2.)
    newtimes2 = wm.getNewTimes(times, 2., phase=0.5)
    assert np.round((np.min(newtimes2) - np.min(newtimes)), 7) == 1.000


def test_getNewVals_for_newrvs_dim():
    """
    The output dimension of newRVs should be the same as the
    input dimension of newtimes
    """
    newtimes = np.arange(10)
    times = np.random.uniform(0, 10, 100)
    rvs = np.random.uniform(-5, 5, 100)
    uncs = np.random.normal(loc=1., scale=0.5, size=100)
    newRVs, newUncs = wm.getNewVals(newtimes, times, rvs, uncs, timebin=1.)
    assert len(newtimes) == len(newRVs)


def test_getNewVals_for_newuncs_dim():
    """
    The output dimension of newRVs should be the same as the
    input dimension of newtimes
    """
    newtimes = np.arange(10)
    times = np.random.uniform(0, 10, 100)
    rvs = np.random.uniform(-5, 5, 100)
    uncs = np.random.normal(loc=1., scale=0.5, size=100)
    newRVs, newUncs = wm.getNewVals(newtimes, times, rvs, uncs, timebin=1.)
    assert len(newtimes) == len(newUncs)


def test_getNewVals_rv_scatter():
    """
    The RV scatter (standard deviation from normally distributed points
    about the mean should be reduced when binning observations down. This
    routine checks that.
    """
    newtimes = np.arange(10)
    times = np.random.uniform(0, 10, 100)
    rvs = np.random.normal(loc=0, scale=5, size=100)
    uncs = np.random.normal(loc=1., scale=0.5, size=100)
    newRVs, newUncs = wm.getNewVals(newtimes, times, rvs, uncs, timebin=1.)
    assert np.std(newRVs) < np.std(rvs)


def test_getNewVals_unc_magnitude():
    """
    The median single measurement precision should be lower
    for the binned data. This function ensures that to be the case.
    """
    newtimes = np.arange(10)
    times = np.random.uniform(0, 10, 100)
    rvs = np.random.normal(loc=0, scale=5, size=100)
    uncs = np.random.normal(loc=1., scale=0.5, size=100)
    newRVs, newUncs = wm.getNewVals(newtimes, times, rvs, uncs, timebin=1.)
    assert np.median(newUncs) < np.median(uncs)


def test_wgtdMeans_number_of_columns():
    """
    Test the number of returned columns
    """
    dfi = pd.DataFrame()
    dfi["JD"] = np.random.uniform(0, 10, 100)
    dfi["mnvel"] = np.random.normal(loc=0, scale=5, size=100)
    dfi["errvel"] = np.random.normal(loc=1., scale=0.5, size=100)
    dfo = wm.wgtdMeans(dfi, timebin=1.0)
    assert len(dfo.columns) == 3


def test_wgtdMeans_number_of_rows():
    """
    Test the number of returned rows
    """
    dfi = pd.DataFrame()
    dfi["JD"] = np.random.uniform(0, 10, 100)
    dfi["mnvel"] = np.random.normal(loc=0, scale=5, size=100)
    dfi["errvel"] = np.random.normal(loc=1., scale=0.5, size=100)
    dfo = wm.wgtdMeans(dfi, timebin=1.0)
    assert len(dfo) >= 9


def test_big_gaps_getNewVals():
    """
    Ensure getNewVals routine can handle big gaps in times
    """
    timebin = 1.
    times = np.concatenate((np.random.uniform(0, 10, 50),
                           np.random.uniform(30, 40, 50)))
    newtimes = wm.getNewTimes(times, timebin)
    rvs = np.random.normal(loc=0, scale=5, size=100)
    uncs = np.random.normal(loc=1., scale=0.5, size=100)
    newRVs, newUncs = wm.getNewVals(newtimes, times, rvs,
                                    uncs, timebin=timebin)
    fins = np.where(np.isfinite(newUncs))
    newRVs = newRVs[fins]
    newUncs = newUncs[fins]
    newtimes = newtimes[fins]
    assert np.median(newUncs) < np.median(uncs)


def test_big_gaps_main_routine():
    """
    Test to make sure the code handles big gaps well
    """
    dfi = pd.DataFrame()
    dfi["JD"] = np.concatenate((np.random.uniform(0, 10, 50),
                               np.random.uniform(40, 50, 50)))
    dfi["mnvel"] = np.random.normal(loc=0, scale=5, size=100)
    dfi["errvel"] = np.random.normal(loc=1., scale=0.5, size=100)
    dfo = wm.wgtdMeans(dfi, timebin=1.0)
    assert len(dfo) >= 9












