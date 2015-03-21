# Welcome to pyutil

###A Python Library of Matt's Useful Utility Files

Project Directory Layout
========================

- **docs**: This documentation
- **pyutil**: The pyutil code
- **site**: The mkdocs build of this site
- **tests**: Unit testing code

Code Documentation
==================

##blazeFit.py

A recursive routine that fits the blaze function of an echelle spectrum. This is useful for cross correlation or equivalent width determination. The algorithm will continue until either the rms reaches `maxrms` or `numcalls` has been reached, whichever comes first.

**Parameters**:
- *wav*: the wavelength
- *spec*: the relative flux
- *maxrms*: the maximum root mean square of the residuals
- *numcalls*: the maximum number of recursive calls to make.

**Returns**:

The returned `fit` array contains the `numpy.polyfit` 7th order polynomial coefficients of the best fit to the continuum.


**Example**:
```python
from pyutil.blazeFit import blazeFit
fit = blazeFit(wav, spec, maxrms, numcalls=150)
```

##connectChironDB.py

A routine for establishing a connection to the CHIRON MySQL database.

**Parameters**:
- *legacy*: [Optional] Boolean argument specifying what will be returned. The default is False, which returns an SQLAlchemy+PyMySQL engine. If True, a PyMySQL connection is returned instead. The SQLAlchemy+PyMySQL engine returned as the default was added because the MySQL connections are deprecated in pandas.

**Returns**:

Either a SQLAlchemy+PyMySQL engine or a PyMySQL connection, depending on the input.

**Examples**:

- For a pymysql connection:

```python
from pyutil import connectChironDB as ccdb
conn = ccdb.connectChironDB(legacy=True)
```

- For an SQLAlchemy `mysql+pymysql` engine:

The MySQL connection flavor has been deprecated in `pandas` and will be removed in a future version. However, MySQL will still be supported through SQLAlchemy. To prepare for this (and get rid of the annoying warning messages), the default object returned from `connectChironDB` is now an SQLAlchemy engine:
```python
from pyutil import connectChironDB as ccdb
engine = ccdb.connectChironDB()
```


##getChironSpec.py

A routine for retrieving and continuum normalizing spectra from the CHIRON Spectrometer. Continuum normalization in this case divides each echelle order by a polynomial fit to the respective order in the master flat field.

**Parameters**:

- *obnm*: The observation name to restore. CHIRON observation names are in the format chiyymmdd.####, where yymmdd are the year, month, and day, and #### is the chronological sequence number that identifies the observation.
- *normalized*: [Optional] Boolean argument specifying if the returned spectrum should be normalized or not. The default is True. If True, the blaze function is determined by fitting the nightly quartz exposures with a polynomial model.

**Returns**:

A CHIRON spectrum that is optionally normalized.

**Example**:
```python
from pyutil.getChironSpec import getChironSpec
normspec = getChironSpec('chi150223.1125', normalized=True)
```

##pearsonBootstrapPvalue.py

A routine for determining the p-value to the Pearson linear correlation coefficient through a Bootstrap analysis.

##wgtdMeans.py

A routine for binning heteroscedastic unevenly sampled time series data. This is similar to velplot in IDL. Specified time bins are used to bin the data. For each bin a weighted mean value is calculated.

**Parameters**:

- *df*: An input pandas DataFrame with at least 3 columns: the observation times, the measurements, and the associated uncertainties.
- *time*: [Optional] The column name of the observation time column in the DataFrame. The default value is "JD".
- *rv*: [Optional] The column name of the observation column. The default value is "mnvel".
- *unc*: [Optional] The default column name for the uncertainty column. If not specified, "errvel" will be used.
- *timebin*: [Optional] The bin size, in the same units as the time column of the input DataFrame. The default value is 0.5.
- *phase*: [Optional] The fractional amount the bin center time will be shifted by. For example, if the input time column is days, and timebin=2, setting a phase=0.5 will shift the times of the returned bins by one day.

**Returns**:

A pandas DataFrame with the binned weighted mean values.

**Example**:
```python
dfout = wgtdMean(dfin, time="JD", rn="mnvel", unc="errvel", timebin=0.5, phase=0)
```
