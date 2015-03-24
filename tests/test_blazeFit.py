#!/usr/bin/env python

"""
PURPOSE: The routines in this file test the blazeFit.py module.

Created on 2015-03-23T16:38:44
"""

from __future__ import division, print_function
import numpy as np
from types import *
#from nose.tools import raises
#import pandas as pd

from pyutil.pyutil import blazeFit as bf

__author__ = "Matt Giguere (github: @mattgiguere)"
__license__ = "MIT"
__version__ = '0.0.1'
__maintainer__ = "Matt Giguere"
__email__ = "matthew.giguere@yale.edu"
__status__ = " Development NOT(Prototype or Production)"


def test_blazeFit():
    """
    Ensure that blazeFit returns a 7th order polynomial
    """
    wav = np.arange(5e3, 5080., 0.02)

    def spec(x):
        return np.exp(-(x - 5040.)**2/1000.)

    polynomial_fit_values = bf.blazeFit(wav, spec(wav), 5e-2)
    assert len(polynomial_fit_values) == 8


def test_with_verbosity():
    wav = np.arange(5e3, 5080., 0.02)

    def spec(x):
        return np.exp(-(x - 5040.)**2/1000.)

    polynomial_fit_values = bf.blazeFit(wav, spec(wav), 5e-2, verbose=True)
    assert len(polynomial_fit_values) == 8


def test_with_noise():
    wav = np.arange(5e3, 5080., 0.02)

    def spec(x):
        normal_noise = np.random.normal(loc=0, scale=0.1, size=len(x))
        blaze_function = np.exp(-(x - 5040.)**2/1000.)
        return blaze_function + normal_noise

    polynomial_fit_values = bf.blazeFit(wav, spec(wav), 5e-2, verbose=True)
    assert len(polynomial_fit_values) == 8


def test_with_show_plot():
    wav = np.arange(5e3, 5080., 0.02)

    def spec(x):
        return np.exp(-(x - 5040.)**2/1000.)

    polynomial_fit_values = bf.blazeFit(wav, spec(wav), 5e-2)#, showplot=True)
    assert len(polynomial_fit_values) == 8


#@raises(ValueError)
#def test_make_function_raise_value_error():


