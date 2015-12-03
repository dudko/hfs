#! /usr/bin/python2.7

""" Define projection and do spatial analysis with all shapefiles from directory """

import arcpy
import glob
import os

""" Constatnts """
WORKDIR = "F:/directory/with/merged/layers"
GRID = "F:/grid.shp"

""" Main """
arcpy.env.workspace = WORKDIR
os.chdir(WORKDIR)

stations = glob.glob("*.shp")
print stations
stations.remove("grid.shp")

print "Define projections."
for station in stations:
    print "Started %s." % station
    arcpy.DefineProjection_management("%s/%s" % (WORKDIR, station),"GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]")    
    print "Done."

print "Spatial."
for station in stations:
    print "Started %s." % station
    arcpy.SpatialJoin_analysis("%s" % GRID, "%s/%s" % (WORKDIR, station), "%s/merged_%s" % (WORKDIR, station),"JOIN_ONE_TO_ONE","KEEP_ALL","""Id "Id" true true false 6 Long 0 6 ,First,#,grid,Id,-1,-1;id_1 "id_1" true true false 11 Double 0 11 ,First,#,merge1,id,-1,-1""","INTERSECT","#","#")
    print "Done."