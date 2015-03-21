#!/usr/bin/env python

"""
Created on 2014-12-03T19:07:01
"""

from __future__ import division, print_function
import sys
import subprocess
from sqlalchemy import create_engine

try:
    import pymysql
except ImportError:
    print('You need pymysql installed')
    sys.exit(1)


__author__ = "Matt Giguere (github: @mattgiguere)"
__maintainer__ = "Matt Giguere"
__email__ = "matthew.giguere@yale.edu"
__status__ = " Development NOT(Prototype or Production)"
__version__ = '0.0.1'


def getAeroDir():
    cmd = 'echo $AeroFSdir'
    #read in the AeroFSdir string and
    adir = subprocess.check_output(cmd, shell=True)
    #chop off the newline character at the end
    adir = adir[0:len(adir)-1]
    return adir


def connectChironDB(legacy=False):
    """PURPOSE:
    A quick and simple function for connecting to the
    CHIRON MySQL database.

    :param legacy: [optional]
        If legacy is set, a PyMySQL connection will be returned.
        Otherwise, a SQLAlchemy engine will be returned. This is
        to handle the deprecated MySQL connections in pandas.
    """
    #retrieve credentials:
    adir = getAeroDir()
    credsf = open(adir+'.credentials/SQL/csaye', 'r')
    creds = credsf.read().split('\n')
    if legacy:
        conn = pymysql.connect(host=creds[0],
                               port=int(creds[1]),
                               user=creds[2],
                               passwd=creds[3],
                               db=creds[4])
        #cur = conn.cursor()
        return conn
    else:
        #example:
        #mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]
        cmd = "mysql+pymysql://"
        cmd += creds[2]+':'
        cmd += creds[3]+'@'
        cmd += creds[0]+'/'
        cmd += creds[4]

        engine = create_engine(cmd)
        return engine
