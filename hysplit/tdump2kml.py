#! /usr/bin/python2.7

""" Convert tdump files to kmls inside of all directories """

""" Modules """
import os
import subprocess
import glob
import sys

""" Constants """
INPUTDIR = 'C:/out'

""" Functions """
def tdump2kml(inputDir):
    """
    Convert tdump files to kmls inside of all directories.
    """
    # Check inputdir
    if not os.path.exists(inputDir):
        print("Entered directory is invalid.")
        sys.exit()

    os.chdir(inputDir)

    # Main loop
    for run in os.walk('.').next()[1]:

        os.chdir(run)

        # Filter tdump files
        files = glob.glob("*.tdump")

        # Conversion
        for entry in files:
            p = subprocess.Popen("C:\\hysplit4\\exec\\trajplot.exe -i%s -o%s.ps -a3 -v1 -l1" % \
                (entry, entry), shell=True, stdout=subprocess.PIPE)
            p.wait()
            os.remove(entry[:-6])
            #p_out = p.communicate()
            #print p_out[0], p_out[1]

        # Move all kmls into dir kmls
        #sys.stdout.flush()
        kmls = glob.glob("*.kml")

        if not os.path.exists("kmls"):
            os.makedirs("kmls")

        for kml in kmls:
            os.rename(kml, "kmls\\%s" % kml)

        # Remove redundant ps files
        pss = glob.glob("*.ps")

        for ps in pss:
            os.remove(ps)

        print "DONE : %s %s\kmls" % (run, os.getcwd())
        os.chdir('../')

""" Run standalone """
if __name__ == '__main__':
    tdump2kml(INPUTDIR)
