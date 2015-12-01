#!/usr/bin/python

from datetime import datetime, timedelta
import os
import subprocess
import csv
from string import Template
import pdb
import sys

from templates import RELEASES, COMMAND

FLEXPART = '/home/dusan/Projects/recetox/usecases/flexpart/install/flexpart_82-3/'
OUTDIR = '/home/dusan/Projects/recetox/usecases/flexpart/install/flexpart_82-3/output'
METEODIR = '/mnt/meteo/'
RUNSCSV = 'runs.csv'

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

  # Load variables from line
  runName = run[0]
  
  relBox = [run[1], run[2], run[3], run[4]]
  relStart = datetime(int(run[5]), int(run[6]), int(run[7]), int(run[8]), int(run[9]))
  relEnd = datetime(int(run[10]), int(run[11]), int(run[12]), int(run[13]), int(run[14]))
  particles = run[15] if "PERMIN" not in run[15] else ((relEnd - relStart).total_seconds() // 60) \
    * int(run[15].split('')[0])

  simStart = datetime(int(run[16]), int(run[17]), int(run[18]), int(run[19]), int(run[20]))
  simEnd = datetime(int(run[21]), int(run[22]), int(run[23]), int(run[24]), int(run[25]))
  simDir = run[26]

  # Create pathnames
  with open("%spathnames" % FLEXPART, "w") as f:
    f.write(FLEXPART+'\n'+OUTDIR+'\n'+METEODIR+'\n'+METEODIR+"AVAILABLE")
    f.close()

  # Create outdir from run name
  if not os.path.exists("%s%s" % (OUTDIR, runName)):
    os.makedir("%s%s" % (OUTDIR, runName))

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

# os.system("vim -c wq /mnt/working/flexpart_indiaLGE/options/COMMAND")

#   os.chdir("/mnt/working/flexpart_indiaLGE/")
#   #os.system("./FLEXPART_GFORTRAN")
#   h = subprocess.Popen("./FLEXPART_GFORTRAN", shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
#   stdout, stderr = h.communicate()

#   with open("log.run", "a") as f:
#     f.write(start.strftime("%Y%m%d %H%M\n"))
#     f.write(end.strftime("%Y%m%d %H%M\n"))
#     f.write(start_run.strftime("%Y%m%d %H%M\n"))
#     f.write(stdout)
#     f.write(stderr)
#     f.write("------------------------------\n\n")
#     f.close()