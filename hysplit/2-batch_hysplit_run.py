# Script automates hysplit daily trajectory computations up to 8 weeks backwards.
# Trajectory model runs by executing binary "hyts_std.exe". Before execution,
# additional configuration files have to be prepared in the current working
# directory.
#
# Global configurations are stored in SETUP.CFG. ASCDATA.CFG holds default
# constant values for land use and roughness length. CONFIG file specifies
# the run and especially paths to to meteo GDAS files.
#
# Runs are defined in the file "runs.csv" in a comma-separated values format.
# Values are in the following order:
# OUTPUT FOLDER, LATITUDE, LONGTITUDE, HEIGHT, YEAR, MONTH, DAY, BACKWARD TIME IN HOURS
#
# Dusan Lago <dusan.lago at gmail.com>
# Tested with Python 2.7.6
# 2014-10-19

"""Modules"""
import csv
import os
import sys
import subprocess
from subprocess import Popen, PIPE
from datetime import date, datetime, timedelta
import time
from sets import Set
import calendar
import math

from templates import ASCDATA, SETUP

""" Constants """
HYSPLIT = 'C:\\hysplit4\\exec\\hyts_std.exe'
OUTDIR = 'C:\\Users\\user\\Desktop\\out\\'
METEODIR = 'D:\\meteo\\'
RUNSCSV = 'C:\\Users\\user\\Desktop\\hfs\\hysplit\\sample_run.csv'
TOPOFMODEL = "15000" # Should be at least 1000

# Check HYSPLIT binary
if not os.path.isfile(HYSPLIT):
    print("Couldn't find HYSPLIT (hyts_std.exe).")
    sys.exit()

""" Additional functions """
# Calculate the week number of month
def weekOfMonth(currentDate):
    return (currentDate.day-1) / 7 + 1

# Create ASCDATA.CFG
def createASCDATA():
    ascdataFile = open('ASCDATA.CFG', 'w')
    ascdataFile.write(ASCDATA)
    ascdataFile.close()

# Create SETUP.CFG
def createSETUP():
    setupFile = open('SETUP.CFG', 'w')
    setupFile.write(SETUP)
    setupFile.close()

"""Main
Run the model for each given hour every day within the date range.
"""

runs = csv.reader(open(RUNSCSV, 'r'))
# First line is header
runs.next()

for line in runs:

    # Load values
    workingDir = line[0]
    lat, lon, height = line[1], line[2], line[3]
    startDate = date(int(line[4]), int(line[5]), int(line[6]))
    endDate = date(int(line[7]), int(line[8]), int(line[9]))
    runtime = int(line[10])
    runtimeWeeks = math.ceil(runtime/(24.0*7))
    hours = line[11].split()

    tsStart = time.time()
    print "STARTED : " + workingDir + datetime.fromtimestamp(tsStart).strftime(' %Y-%b-%d %H:%M:%S')

    # Make dir for current run
    if not os.path.exists(OUTDIR + workingDir):
        os.makedirs(OUTDIR + workingDir)
    os.chdir(OUTDIR + workingDir)

    # Create log file
    log = open('RUN.LOG', 'w')
    # ASCDATA.CFG
    createASCDATA()
    # SETUP.CFG
    createSETUP()

    while startDate <= endDate:
        for hour in hours:
            # Create CONTROL
            control = open('CONTROL', 'w')
            control.write(startDate.strftime('%y %m %d ') + hour + '\n')
            control.write('1\n')
            control.write(lat + ' ' + lon + ' ' + height + '\n')
            control.write(str(runtime) + '\n')
            control.write('0\n') # vertical motion
            control.write(TOPOFMODEL + '\n')

            # Add sufficient number of meteo files
            if runtimeWeeks > 0:
                meteoDateEnd = startDate + timedelta(weeks=runtimeWeeks)
                meteoDateStart = startDate
            else:
                meteoDateStart = startDate - timedelta(weeks=abs(runtimeWeeks))
                meteoDateEnd = startDate

            # Set of all meteo files is created
            meteoFiles = Set()

            while meteoDateStart <= meteoDateEnd:
                meteoFiles.add('gdas1.' + meteoDateStart.strftime('%b%y').lower() \
                    + '.w' + str(weekOfMonth(meteoDateStart)))
                meteoDateStart = meteoDateStart + timedelta(days=1)

            control.write(str(len(meteoFiles)) + '\n')

            for meteoFile in meteoFiles:
                if not os.path.isfile(METEODIR + "\\" + meteoFile):
                   print "Missing " + METEODIR + "\\" + meteoFile
                   raw_input()
                   break
                control.write(METEODIR + '\\\n')
                control.write(meteoFile + '\n')

            # Output location
            control.write(OUTDIR + workingDir + '\\\n')
            control.write(startDate.strftime('%y%m%d')+hour+'.tdump')
            control.close()

            """ Run model and log its output """
            # Hide poping window
            startupinfo = None
            if os.name == 'nt':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess._subprocess.STARTF_USESHOWWINDOW
            run = Popen(HYSPLIT, stdout=PIPE, stderr=PIPE, startupinfo=startupinfo)
            runOut = run.communicate()
            print "DONE : " + startDate.strftime('%y%m%d') + hour + ".tdump"

            log.write(runOut[0])
            log.write(runOut[1])

        startDate += timedelta(days=1)
    os.chdir('../')
    log.close()
    print "FINISHED : " + datetime.fromtimestamp(time.time()).strftime(' %Y-%b-%d %H:%M:%S')

# Keep terminal open after execution
raw_input("Press Enter to terminate the script.")
