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


def getChironSpec(obnm, normalized=True, slit='slit', normmech='flat'):
    """PURPOSE: To retrieve a CHIRON spectrum given the observation
    name (obnm)."""

    #extract the date (yymmdd) from the obnm:
    date = re.search(r'chi(\d{6})', obnm).group(1)

    #extract the core of the obnm. This will make the code more
    #robust, allowing people to enter the obnm with or without
    #the 'a' or 'chi' or 'fits', etc.
    #output obnm is in the format 'chiyymmdd.####'
    obnm = re.search(r'(chi\d{6}\.\d{4})', obnm).group(1)

    scihdu = fits.open('/tous/mir7/fitspec/'+date+'/a'+obnm+'.fits')
    scidata = scihdu[0].data

    if normalized:
        #generate the flat filename:
        flatfn = '/tous/mir7/flats/chi'+date+'.'+slit+'flat.fits'
        flathdu = fits.open(flatfn)
        flatdata = flathdu[0].data

        #create a 2D array to store the output (wav/spec, #orders, px/order):
        normspecout = np.zeros([2, flatdata.shape[1], flatdata.shape[2]])

        #cycle through orders
        for ord in range(flatdata.shape[1]):
            #now retrieve the normalized polynomial fit to the master flat:
            normfit = flatdata[2, 61 - ord, :]/np.max(flatdata[2, 61 - ord, :])

            #superimpose stellar spec
            normspec_init = scidata[ord, :, 1]/np.max(scidata[ord, :, 1])
            normspec = normspec_init/normfit[::-1]

            #determine the number of maximum values to
            #use in the normalization. In this case we
            #will use the top 0.5%, which corresponds
            #to 16 elements for CHIRON:
            nummax = np.int(np.ceil(0.005 * len(normspec)))
            #now sort normspec and find the mean of the
            #`nummax` highest values in the old normspec
            mnhghval = np.mean(np.sort(normspec)[-nummax:-1])
            #now renormalize by that value:
            normspecout[1, ord, :] = normspec / mnhghval
            normspecout[0, ord, :] = scidata[ord, :, 0]
        return normspecout
    else:
        return scidata


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
 