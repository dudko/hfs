#! /usr/bin/python2.7

""" Combine functions as they follow in batch processing. """

from batchRunHysplit import runBatch
from tdump2shp import tdump2shp
from tdump2kml import tdump2kml
from mergeShapes import mergeShapes

""" Constants """
OUTDIR = 'C:/out/'
METEODIR = 'D:/meteo/'
RUNSCSV = 'C:/Users/user/Desktop/hfs/hysplit/sample_runs.csv'

""" Main """
print "== BATCH RUN =="
runBatch(OUTDIR, METEODIR, RUNSCSV)
print "== TDUMP2SHP =="
tdump2shp(OUTDIR)
print "== TDUMP2KML =="
tdump2kml(OUTDIR)
print "== MERGING SHAPEFILES =="
mergeShapes(OUTDIR)
