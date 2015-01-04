#!/usr/bin/env python

"""
Created on 2014-11-10T15:05:21
"""

from __future__ import division, print_function
import sys

try:
    import numpy as np
except ImportError:
    print('You need numpy installed')
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

params = {
    #'backend': 'png',
    'axes.linewidth': 1.5,
    'axes.labelsize': 24,
    'font.size': 22,
    'legend.fontsize': 14,
    'xtick.labelsize': 16,
    'ytick.labelsize': 16,
    'text.usetex': False,
    'font.family': 'Arial Black'
}
plt.rcParams.update(params)


def blazeFit(wav, spec, maxrms, numcalls=10, curcall=0,
             verbose=False, showplot=False):
    """PURPOSE: To fit the continuum of an order of an
    echelle spectrum to model the Blaze Function.
    INPUTS:
    WAV: The wavelength
    SPEC: The spectrum. This should be the same number of elements
    (and corrsepond to) the input wavelength array (wav).
    MAXRMS: The threshold criteria for the fit in normalized rms.
    For example, a threshold of 0.01 will keep iterating until
    the rms of the residuals of dividing the continuum pixels
    by the Blaze Function comes out to 1%.
    NUMCALLS: The maximum number of recursive iterations to execute.
    CURCALL: Store the current iteration for recursive purposes.
    VERBOSE: Set this to True to print out the iteration, residual
    rms and the threshold value.
    SHOWPLOT: Set this to True to produce a plot of the spectrum,
    threshold and continuum at every iteration.
    """
    #get wavelength range:
    wavspread = max(wav) - min(wav)

    #center wavelength range about zero:
    wavcent = wav - min(wav) - wavspread/2.

    #normalize the spectrum:
    normspec = spec/max(spec)

    #fit a polynomial to the data:
    z = np.polyfit(wavcent, normspec, 7)

    #make a function based on those polynomial coefficients:
    cfit = np.poly1d(z)

    #make a lower threshold that is offset below the continuum fit. All points
    #below this fit (i.e. spectral lines) will be excluded from the fit in the
    #next iteration.
    thresh = cfit(wavcent) - (0.5 * (1. / (curcall + 1)))

    if (showplot is True):
        #plot the original spectrum:
        plt.plot(wavcent, normspec)
        #overplot the continuum fit
        plt.plot(wavcent, cfit(wavcent))
        plt.plot(wavcent, thresh)

    mask = np.where(normspec > thresh)[0]

    residrms = np.std(normspec/cfit(wavcent))
    if (verbose is True):
        print('now in iteration {0}'.format(curcall))
        print('residrms is now {0:.5f}'.format(residrms))
        print('maxrms is {0})'.format(maxrms))
        #print('z is: {}'.format(z))

    if ((curcall < numcalls) and (residrms > maxrms)):
        z = blazeFit(wavcent[mask], normspec[mask], maxrms,
                     numcalls=numcalls, curcall=curcall+1)

    #now un-center the wavelength range:
    #if curcall == 0:
        #z[-1] = z[-1] - min(wav) - wavspread/2.

    return z
