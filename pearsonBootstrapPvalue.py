#!/usr/bin/env python

"""
Created on 2015-01-02T12:34:32
"""

from __future__ import division, print_function
import sys

try:
    from scipy.stats.stats import pearsonr
except ImportError:
    print('You need scipy installed.')
    sys.exit(1)

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


def pearsonBootstrapPvalue(xarr, yarr, numsamp=1e4, plot=False):
    """Calculate and return the pearson correlation coefficient and
       associated p-value using a bootstrap approach.

        ##Parameters
        ----------

        Input:
        xarr: (N,) array_like
        yarr: (N,) array_like

        Optional Input:
        numsamp: The number of bootstrap scrambling samplings to
            perform when computing the p-value. The default is 1e4.
        plot: generate histogram plot showing the distribution of
            rho values from the bootstrap analysis with the values
            more extreme than the original p-value highlighted in
            orange.

        Output:
        rho: the original Pearson linear correlation coefficient based
            on the unscrambled data set
        pval: the two-tailed boostrap MC with replacement generated p-value
    """
    rhoinit = pearsonr(xarr, yarr)
    ynew = np.copy(yarr)
    numsamp = float(numsamp)
    rhoarr = np.zeros(numsamp)
    for i in np.arange(numsamp):
        np.random.shuffle(ynew)
        (rhoarr[i], pt) = pearsonr(xarr, ynew)

    numgreater = len(np.where(np.abs(rhoarr) >= np.abs(rhoinit[0]))[0])
    pval = numgreater / numsamp
    #if rhoinit[0] < 0:
    #    pval = len(np.where(rhoarr <= rhoinit[0])[0]) / numsamp * 2.
    print('number of permutations greater than the original: {0}'.format(numgreater))
    if plot:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.hist(rhoarr, bins=50, color='#6D92D2', edgecolor='#164BA7')
        if (numgreater > 2):
            #superimpose the permutations greater than the original in salmon:
            plt.hist(rhoarr[np.abs(rhoarr) >= np.abs(rhoinit[0])], bins=50, color='#FD9D76', edgecolor='#FC4F1A') 
            #superimpose the permutations greater than the original in aquamarine:
            #plt.hist(rhoarr[np.abs(rhoarr) >= np.abs(rhoinit[0])], bins=50, color='#66D5AA', edgecolor='#1DAB6D') 
        plt.xlabel(r'Pearson Correlation Coefficient ($\rho$)')
        ax.set_ylabel('Number of Permutations')
        plt.axvline(rhoinit[0], color='#FC4F1A', alpha=0.75, lw=2.)
        plt.axvline(-1. * rhoinit[0], color='#FC4F1A', alpha=0.75, lw=2.)
        textstr = '$\\rho$ = {0:.2f} \n p-value = {1:.4f}'.format(rhoinit[0], pval)
        props = dict(boxstyle='square', facecolor='white', alpha=0.5)
        ax.text(0.05, 0.95, textstr, transform=ax.transAxes, bbox=props,
                 fontsize=14, verticalalignment='top')

    return rhoinit[0], pval
