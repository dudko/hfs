#! /usr/bin/python2.7

""" Convert tdump files to shapefiles inside of all directories """

""" Modules """
import os
import subprocess
import glob

""" Constants """
INPUTDIR = 'C:/out'

""" Functions """
def tdump2shp(inputDir):
    """
    For all directories in inputDir convert tdumps to shps.
    Output files are stored inside of each directory in dir shapes."
    """
    os.chdir(inputDir)

    for run in os.walk('.').next()[1]:

        os.chdir(run)

        if not os.path.exists("shapes"):
            os.makedirs("shapes")

        # Filter tdump files
        files = glob.glob("./*.tdump")

        for entry in files:
            hSource = open(entry, "r").readlines()
            out = open("shapes/%s.gis" % entry, "w")

            # Set the number of lines to be ommited. Based on the number of meteo files.
            offset = int(hSource[0].split()[0]) + 4

            if len(hSource) > offset:
                #pdb.set_trace()
                out.write("  1, %s %s\n" % (hSource[offset].split()[10], \
                    hSource[offset].split()[9]))

                for line in hSource[offset:]:
                    words = line.split()
                    out.write("%s %s\n" % (words[10], words[9]))

                out.write("END")
                out.close()

                os.chdir("shapes")

                # Convert GIS file to shape file.
                subprocess.Popen("C:\\hysplit4\\exec\\ascii2shp.exe %s lines < %s.gis" % \
                    (entry, entry), shell=True, stdout=subprocess.PIPE)
                os.chdir("..")

        # Feedback
        print "DONE : %s %s\shapes" % (run, os.getcwd())

        os.chdir("..")

""" Run standalone """
if __name__ == '__main__':
    tdump2shp(INPUTDIR)
