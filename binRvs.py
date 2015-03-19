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

__author__ = "Matt Giguere (github: @mattgiguere)"
__maintainer__ = "Matt Giguere"
__email__ = "matthew.giguere@yale.edu"
__status__ = " Development NOT(Prototype or Production)"
__version__ = '0.0.1'


def getNewTimes(times, timebin):
    """Return the new time array"""
    numnewtimes = (np.max(times) - np.min(times))/timebin
    newtimes = np.linspace(np.min(times), np.max(times), numnewtimes)
    return newtimes


def binRvs(df, time="JD", rv="mnvel", unc="errvel", timebin=0.5, phase=0):
    """
    PURPOSE: A routine to bin RV measurements similar to velplot
    in IDL.
    """
    times = df[time]
    rvs = df[rv]
    uncs = df[unc]

    newtimes = getNewTimes(times, timebin)

    dfdown = df
    return dfdown
