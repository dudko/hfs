#! /usr/bin/python2.7

""" Convert tdump files to kmls inside of all directories """

""" Modules """
import os
import subprocess
import glob
import sys

""" Constants """
INPUTDIR = '/tmp/tdumps'

""" Functions """
def tdump2kml(inputDir):
    """
    Convert tdump files to kmls inside of all directories.
    """
    # Check inputdir
    if not os.path.exists(inputDir):
        print("Entered directory is invalid.")
        sys.exit()

    print "\n * starting to convert\n"

    os.chdir(inputDir)

    # Main loop
    for run in os.walk('.').next()[1]:

        os.chdir(run)

        print "\t * converting %s" % run

        # Filter tdump files
        files = glob.glob("0*")
        files.extend(glob.glob("1*"))

        # Conversion
        for entry in files:
            p = subprocess.Popen("C:\\hysplit4\\exec\\trajplot.exe -i%s -o%s.ps -a3 -v1 -l1" % \
                (entry, entry), shell=True, stdout=subprocess.PIPE)
            p.wait()
            
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

        os.chdir('../')    

""" Run standalone """
if __name__ == '__main__':
    tdump2kml(INPUTDIR)