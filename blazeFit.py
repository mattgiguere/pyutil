#!/usr/bin/env python

"""
Created on 2014-11-10T15:05:21
"""

from __future__ import division, print_function
import sys
import argparse

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
    'axes.font': 'sans-serif',
    'axes.fontweight': 'bold',
    'text.fontsize': 22,
    'legend.fontsize': 14,
    'xtick.labelsize': 16,
    'ytick.labelsize': 16,
    'text.usetex': False,
    'font.family': 'Arial Black'
}
plt.rcParams.update(params)


def blazeFit(wav, spec):
    """PURPOSE: To fit the continuum of an order of an echelle spectrum
    to model the Blaze Function."""


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='argparse object.')
    parser.add_argument(
        'arg1',
        help='This argument does something.')
    parser.add_argument(
        'arg2',
        help='This argument does something else. By specifying ' +
             'the "nargs=>" makes this argument not required.',
             nargs='?')
    if len(sys.argv) > 3:
        print('use the command')
        print('python blazeFit.py arg1 arg2')
        sys.exit(2)

    args = parser.parse_args()

    blazeFit(int(args.arg1), args.arg2)
 