#! /usr/bin/python2.7

""" Combine functions as they follow in batch processing. """

from batchRunHysplit import runBatch
from tdump2shp import tdump2shp
from tdump2kml import tdump2kml
from mergeShapes import mergeShapes

""" Constants """
OUTDIR = 'C:\\Users\\user\\Desktop\\out\\'
METEODIR = 'D:\\meteo\\'
RUNSCSV = 'C:\\Users\\user\\Desktop\\hfs\\hysplit\\sample_run.csv'

""" Main """
runBatch(OUTDIR, METEODIR, RUNSCSV)
tdump2shp(OUTDIR)
tdump2kml(OUTDIR)
mergeShapes(OUTDIR)