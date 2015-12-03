#! /usr/bin/python2.7

""" Merge all shapefiles inside of all directories containing shape files """

""" Modules """
import glob
import os
import sys
import shapefile

""" Constants """
INPUTDIR = 'C:\out'

""" Functions """
def mergeShapes(inputDir):
    """
    Merge all shapefiles inside of all directories of inputDir
    """
    os.chdir(inputDir)

    for run in os.walk('.').next()[1]:
        os.chdir(run + "\\shapes")

        merged_shapes = shapefile.Writer()
        shape_files = glob.glob("*.shp")


        for shape_file in shape_files:
            reader = shapefile.Reader(shape_file)
            merged_shapes._shapes.extend(reader.shapes())
            merged_shapes.records.extend(reader.records())

        merged_shapes.fields = list(reader.fields)
        merged_shapes.save('MERGED_%s.shp"'% run)

        # Feedback
        print "MERGED : %s\MERGED_%s.shp" % (os.getcwd(), run)

        os.chdir("../../")

""" Run standalone """
if __name__ == '__main__':
    mergeShapes(INPUTDIR)
