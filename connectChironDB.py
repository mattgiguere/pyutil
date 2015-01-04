#!/usr/bin/env python

"""
Created on 2014-12-03T19:07:01
"""

from __future__ import division, print_function
import sys
import argparse
import subprocess

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


def connectChironDB():
    """connect to the database"""
    #retrieve credentials:
    adir = getAeroDir()
    credsf = open(adir+'.credentials/SQL/csaye', 'r')
    creds = credsf.read().split('\n')
    conn = pymysql.connect(host=creds[0],
                           port=int(creds[1]),
                           user=creds[2],
                           passwd=creds[3],
                           db=creds[4])
    #cur = conn.cursor()
    return conn


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
        print('python connectChironDB.py arg1 arg2')
        sys.exit(2)

    args = parser.parse_args()

    connectChironDB(int(args.arg1), args.arg2)
 