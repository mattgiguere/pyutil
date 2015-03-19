#!/usr/bin/env python

"""
Created on 2015-03-19T16:19:41
"""

from __future__ import division, print_function
import sys
import argparse
import pyutil.binRvs as br

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


def test_getNewTimes_one_day_bin_ten_days():
    """
    Test to make sure `getNewTimes` returns ten times
    when 75 times are entered over a ten day spane with
    one day binning in place.
    """
    times = np.random.uniform(0, 11, 75)
    newtimes = br.getNewTimes(times, 1.)
    print(len(newtimes))
    assert len(newtimes) == 10

