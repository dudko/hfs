#! /usr/bin/python2.7

""" Combine functions as they follow in batch processing. """

from batchRunHysplit import runBatch
from tdump2shp import tdump2shp
from tdump2kml import tdump2kml
from mergeShapes import mergeShapes
# from meteoDownloader import downloadMeteo

""" Constants """
METEO_START = (12, 2012)
METEO_END = (1, 2013)
OUTDIR = 'C:/out/'
METEODIR = 'D:/meteo/'
RUNSCSV = 'C:/Users/user/Desktop/hfs-master/hysplit/sample_runs.csv'

""" Main """
# print "== DOWNLOAD METEO DATA =="
# downloadMeteo(METEO_START, METEO_END, METEODIR)
print "== BATCH RUN =="
runBatch(OUTDIR, METEODIR, RUNSCSV)
print "== TDUMP2SHP =="
tdump2shp(OUTDIR)
print "== TDUMP2KML =="
tdump2kml(OUTDIR)
print "== MERGING SHAPEFILES =="
mergeShapes(OUTDIR)
