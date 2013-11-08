#!/usr/bin/env python
"""FVS Batch 

Looks in a directory, 
finds all subdirectories (which are presumed to be a data dir for the fvs script),
and fires off a celery task for each

Usage:
    batch.py [BATCHDIR]
    batch.py (-h | --help)
    batch.py --version

Options:
    -h --help     Show this screen.
    --version     Show version.
"""
from docopt import docopt
import os
import sys
from run_fvs import apply_fvs_to_plotdir


def get_immediate_subdirectories(dir):
    return [name for name in os.listdir(dir) if os.path.isdir(os.path.join(dir, name))]

if __name__ == "__main__":
    args = docopt(__doc__, version='FVS Batch 1.0')

    batchdir = args['BATCHDIR']
    if not batchdir:
        batchdir = os.path.curdir
    batchdir = os.path.abspath(batchdir)
    plotsdir = os.path.join(batchdir, 'plots')
    if not os.path.exists(plotsdir):
        print "ERROR:: No plots directory found in %s; Run build_keys first" % batchdir
        sys.exit

    datadirs = get_immediate_subdirectories(plotsdir)
    if len(datadirs) == 0:
        print "ERROR:: Plots directory '%s' doesn't contain any subdirectories" % batchdir
        sys.exit(1)

    i = 0
    j = 1000
    n = len(datadirs)
    for datadir in datadirs:
        # output every jth iteration
        i += 1
        if i % j == 0:
            print "  sent %s of %s" % (i, n)

        plotdir = os.path.join(plotsdir, datadir) 
        print plotdir
        apply_fvs_to_plotdir(plotdir)

    print "DONE!"