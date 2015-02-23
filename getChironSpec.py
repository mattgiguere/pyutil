#!/usr/bin/env python

"""
Created on 2015-02-22T19:41:02
"""

from __future__ import division, print_function
import sys
import argparse
import re

try:
    import numpy as np
except ImportError:
    print('You need numpy installed')
    sys.exit(1)

try:
    from astropy.io import fits
except ImportError:
    print('You need astropy installed')
    sys.exit(1)

try:
    import matplotlib.pyplot as plt
    got_mpl = True
except ImportError:
    print('You need matplotlib installed to get a plot')
    got_mpl = False

__author__ = "Matt Giguere (github: @mattgiguere)"
__maintainer__ = "Matt Giguere"
__email__ = "matthew.giguere@yale.edu"
__status__ = " Development NOT(Prototype or Production)"
__version__ = '0.0.1'


def getChironSpec(obnm, normalized=True, slit='slit'):
    """PURPOSE: To retrieve a CHIRON spectrum given the observation
    name (obnm)."""

#    #extract the date (yymmdd) from the obnm:
    date = re.search(r'chi(\d{6})', obnm).group(1)

    #extract the core of the obnm. This will make the code more 
    #robust, allowing people to enter the obnm with or without
    #the 'a' or 'chi' or 'fits', etc.
    #output obnm is in the format 'chiyymmdd.####'
    obnm = re.search(r'(chi\d{6}\.\d{4})', obnm).group(1)

    if normalized:
        #generate the flat filename:
        flatfn = '/tous/mir7/flats/chi'+date+'.'+slit+'flat.fits'
        flathdu = fits.open(flatfn)
        flatdata = flathdu[0].data

    scihdu = fits.open('/tous/mir7/fitspec/'+date'/a'+obnm+'.fits')
    scidata = scihdu[0].data








if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='argparse object.')
    parser.add_argument(
        'obnm',
        help='The observation name of the spectrum to be returned.')
    parser.add_argument(
        '-n', '--normalized',
        help='Set whether you want the returned spectrum ' +
             'to be normalized or not.',
             nargs='?')
    if len(sys.argv) > 3:
        print('use the command')
        print('python filename.py tablenum columnnum')
        sys.exit(2)

    args = parser.parse_args()

    if args.normalized:
        normalized = True
    else:
        normalized = False

    getChironSpec(args.obnm, normalized=normalized)
 