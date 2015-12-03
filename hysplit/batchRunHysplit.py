#! /usr/bin/python2.7

""" Script automates HYSPLIT trajectory model. The model runs
for each given hour every day within the date range. Runs are
defined in the file CSV file and must follow the format as in
sample_runs.csv.
Can be used as a module or as a standalone program.
"""

""" Modules """
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
HYSPLIT = 'C:/hysplit4/exec/hyts_std.exe'
OUTDIR = 'C:/out/'
METEODIR = 'D:/meteo/'
RUNSCSV = 'C:/Users/user/Desktop/hfs/hysplit/sample_runs.csv'
TOPOFMODEL = "15000" # Should be at least 1000

# Check HYSPLIT binary
if not os.path.isfile(HYSPLIT):
    print("Couldn't find HYSPLIT (hyts_std.exe).")
    sys.exit()

""" Functions """
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

def runBatch(outdir, meteodir, runCsv):
    """
    Run the model for each given hour every day within the date range.
    """
    runs = csv.reader(open(runCsv, 'r'))
    # First line is header
    runs.next()

    for line in runs:

        # Load values
        workingDir = line[0]
        lat, lon, height = line[1], line[2], line[3]
        startDate = date(int(line[4]), int(line[5]), int(line[6]))
        endDate = date(int(line[7]), int(line[8]), int(line[9]))
        runtime = int(line[11])
        runtimeWeeks = math.ceil(runtime/(24.0*7))
        hours = line[10].split()

        tsStart = time.time()
        print "STARTED : " + workingDir + datetime.fromtimestamp(tsStart).strftime(' %Y-%b-%d %H:%M:%S')

        # Make dir for current run
        if not os.path.exists(outdir + workingDir):
            os.makedirs(outdir + workingDir)
        os.chdir(outdir + workingDir)

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
                    if not os.path.isfile(meteodir + "\\" + meteoFile):
                       print "Missing " + meteodir + "\\" + meteoFile
                       raw_input()
                       break
                    control.write(meteodir + '\\\n')
                    control.write(meteoFile + '\n')

                # Output location
                control.write(outdir + workingDir + '\\\n')
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

""" Run standalone """
if __name__ == '__main__':
    runBatch(OUTDIR, METEODIR, RUNSCSV)
