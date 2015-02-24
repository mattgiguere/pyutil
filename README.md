pyutil
======

####Python Utility Files
[![Build Status](https://travis-ci.org/mattgiguere/pyutil.svg?branch=master)](https://travis-ci.org/mattgiguere/pyutil)

This repository contains python utility files that I have found useful for a number of projects. Most of these routines are related to CHIRON high resolution fiber fed spectroscopy, but you may find some are useful well outside of astronomy/science/academia.

Below are descriptions for the routines in this repository.

- **blazeFit.py**: A recursive routine that fits the blaze function of an echelle spectrum. This is useful for cross correlation or equivalent width determination.
Example:
```python
from pyutil.blazeFit import blazeFit
fit = blazeFit(wav, spec, maxrms, numcalls=150)
```
The resulting `fit` array contains the `numpy.polyfit` 7th order polynomial coefficients to the best fit to the continuum, `wav` is the wavelength, `spec` is the relative flux, `maxrms` is the maximum root mean square of the residuals, and `numcalls` is the maximum number of recursive calls to make. The algorithm will continue until either the rms reaches `maxrms` or `numcalls` has been reached, whichever comes first.


- **connectChironDB.py**: A routine for establishing a connection to the CHIRON MySQL database.
Examples:
for an SQLAlchemy `mysql+pymysql` engine:
for a pymysql connection:
```python
from pyutil import connectChironDB as ccdb
conn = ccdb.connectChironDB(legacy=True)
```
The MySQL connection flavor has been deprecated in `pandas` and will be removed in a future version. However, MySQL will still be supported through SQLAlchemy. To prepare for this (and get rid of the annoying warning messages), the default object returned from `connectChironDB` is now an SQLAlchemy engine:
```python
from pyutil import connectChironDB as ccdb
engine = ccdb.connectChironDB()
```
- **getChironSpec.py**: A routine for retrieving and continuum normalizing spectra from the CHIRON Spectrometer. Continuum normalization in this case divides each echelle order by a polynomial fit to the respective order in the master flat field. An example of using `getChironSpec` is shown below.
```python
from pyutil.getChironSpec import getChironSpec
normspec = getChironSpec('chi150223.1125', normalized=True)
```

- **pearsonBootstrapPvalue.py**: A routine for determining the p-value to the Pearson linear correlation coefficient through a Bootstrap analysis.
