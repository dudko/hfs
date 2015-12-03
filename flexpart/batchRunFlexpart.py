#! /usr/bin/python2.7

""" Run flexpart in batch using input data from cvs file. """

""" Modules """
import os
import sys
import csv
import time
import subprocess
from templates import RELEASES, COMMAND
from string import Template
from datetime import datetime

""" Constants """
FLEXPART = '/mnt/working/demo/flexpart/'
OUTDIR = '/mnt/working/demo/out/'
METEODIR = '/mnt/meteo/indiaLGE/'
RUNSCSV = '/mnt/working/demo/sample_runs.csv'

# Check if all paths are correcly ended with /
for path in [FLEXPART, OUTDIR, METEODIR]:
  if path[-1] != "/":
    print "Missing / in %s." % path
    sys.exit()  

# Check FLEXPART executable
if not os.path.isfile('%sFLEXPART_GFORTRAN' % FLEXPART):
  print("Couldn't find FLEXPART executable.")
  sys.exit()

if not os.path.isdir(OUTDIR):
  os.makedirs(OUTDIR)  

""" Start batch execution """
runs = csv.reader(open(RUNSCSV, 'r'))

# Omit first two lines with headers
runs.next()
runs.next()

for run in runs:

  # Create timestamp
  tsStart = time.time()

  # Load variables from line
  runName = run[0]
  
  relBox = [run[1], run[2], run[3], run[4]]
  relStart = datetime(int(run[5]), int(run[6]), int(run[7]), int(run[8]), int(run[9]))
  relEnd = datetime(int(run[10]), int(run[11]), int(run[12]), int(run[13]), int(run[14]))
  particles = run[15] if "PERMIN" not in run[15] else int(((relEnd - relStart).total_seconds() // 60) \
    * int(run[15].split()[0]))

  simStart = datetime(int(run[16]), int(run[17]), int(run[18]), int(run[19]), int(run[20]))
  simEnd = datetime(int(run[21]), int(run[22]), int(run[23]), int(run[24]), int(run[25]))
  simDir = run[26]

  # Create pathnames
  with open("%spathnames" % FLEXPART, "w") as f:
    f.write(FLEXPART+"options/\n"+OUTDIR+runName+"/\n"+METEODIR+"\n"+METEODIR+"AVAILABLE")
    f.close()

  # Create outdir from run name
  if not os.path.exists("%s%s" % (OUTDIR, runName)):
    os.mkdir("%s%s" % (OUTDIR, runName))

  # Generate RELEASES and COMMAND
  with open("%soptions/RELEASES" % FLEXPART, "w") as f:
    f.write(RELEASES.substitute(relStartDate=relStart.strftime('%Y%m%d'), relStartTime=relStart.strftime('%H%M'), \
      relEndDate=relEnd.strftime('%Y%m%d'), relEndTime=relEnd.strftime('%H%M'), relBoxLonLL=relBox[0], \
      relBoxLatLL=relBox[1], relBoxLonUR=relBox[2], relBoxLatRL=relBox[3], particles=particles))
    f.close()

  with open("%soptions/COMMAND" % FLEXPART, "w") as f:
    f.write(COMMAND.substitute(simStartDate=simStart.strftime('%Y%m%d'), simStartTime=simStart.strftime('%H%M'), \
      simEndDate=simEnd.strftime('%Y%m%d'), simEndTime=simEnd.strftime('%H%M'), simDir=simDir))
    f.close()

  # Execute FLEXPART_GFORTRAN
  print "EXECUTING : %s" % runName
  print datetime.fromtimestamp(tsStart).strftime('STARTED : %Y-%b-%d %H:%M:%S')
  os.chdir(FLEXPART)
  flexProc = subprocess.Popen("./FLEXPART_GFORTRAN", shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
  stdout, stderr = flexProc.communicate()

  tsEnd = time.time()
  
  print "OUTPUT : " + stdout + stderr
  print datetime.fromtimestamp(tsEnd).strftime('DONE : %Y-%b-%d %H:%M:%S\n')

  # Log run
  with open("%slog.run" % FLEXPART, "a") as f:
    f.write("RUNNAME : %s\n" % runName)
    f.write("TIMESTAMP : " + datetime.fromtimestamp(tsEnd).strftime('%Y-%m-%d %H:%M:%S\n'))
    f.write("RELEASE : " + relStart.strftime("%Y%m%d %H%M - ") + relEnd.strftime("%Y%m%d %H%M\n"))
    f.write("SIMULATION : " + simStart.strftime("%Y%m%d %H%M - ") + simEnd.strftime("%Y%m%d %H%M\n"))
    f.write("STDOUT : " + stdout)
    f.write("STDERR : " + stderr)
    f.write("\n------------------------------\n")
    f.close()