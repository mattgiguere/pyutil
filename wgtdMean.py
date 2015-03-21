#!/usr/bin/env python

"""
Created on 2015-03-19T15:55:54
"""

from __future__ import division, print_function
import sys

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
__license__ = "MIT"
__version__ = '1.0.0'
__maintainer__ = "Matt Giguere"
__email__ = "matthew.giguere@yale.edu"
__status__ = "Production"


def getNewTimes(times, timebin, phase=0):
    """Return the new time array"""
    newtimes = np.arange(np.min(times), np.max(times), timebin)
    return newtimes + phase * timebin


def getNewVals(newtimes, times, rvs, uncs, timebin):
    """Given all the other parameters, this function returns the
    binned weighted RVs and uncertainties"""
    newRvs = np.zeros(len(newtimes))
    newUncs = np.zeros(len(newtimes))

    for idx, ntm in enumerate(newtimes):
        inbin = np.where((times >= (ntm - timebin/2)) &
                         (times < (ntm + timebin/2)))[0]
        #print('idx: {}, inbin: {}, len {}'.format(idx, inbin, len(inbin)))

        if len(inbin) > 0:
            nwgts = uncs[inbin] / np.sum(uncs[inbin])
            newRvs[idx] = np.sum(rvs[inbin] * nwgts)
            newUncs[idx] = np.mean(uncs[inbin])/np.sqrt(len(inbin))
        else:
            newRvs[idx] = None
            newUncs[idx] = None

    return newRvs, newUncs


def wgtdMeans(df, time="JD", rv="mnvel", unc="errvel", timebin=0.5, phase=0):
    """
    PURPOSE: A routine to bin unevenly sampled heteroscedastic time
    series data, and output weighted mean of each bin. This routine
    is similar to velplot in IDL.

    :param df:
        The input pandas DataFrame with at least three columns:
            - observation times
            - observations
            - uncertainties

    :param time: [Optional]
        The name of the observation time column. The default value
        is "JD".

    :param rv: [Optional]
        The name of the observations column. The default value
        is "rv".

    :param unc: [Optional]
        The name of the uncertainties column. If not set, "errvel"
        is assumed for the column name.

    :param timebin: [Optional]
        The duration to bin the data over. The units should be the
        same as the time column. If not set, 0.5 is assumed.

    :param phase: [Optional]
        The phase offset of the time of the center of the bin. For
        example, if you specify 3 day bins, and phase=0.5, then the
        center of the bin will be shifted by 1.5 days from the
        minimum value in the time column.
    """
    times = df[time].values
    rvs = df[rv].values
    uncs = df[unc].values

    newtimes = getNewTimes(times, timebin, phase=phase)
    newRvs, newUncs = getNewVals(newtimes, times, rvs, uncs, timebin)

    dfnew = pd.DataFrame()
    dfnew[time] = newtimes
    dfnew[rv] = newRvs
    dfnew[unc] = newUncs
    return dfnew
