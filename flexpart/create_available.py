# Generate AVAILABLE file for meteo files in entered directory.
# AVAILABLE is written to this dir.
#
# Dusan Lago <dusan.lago at gmail.com>
# Tested with Python 2.7.6
# 2015-12-01

import glob
import os
import sys

"""Constants"""
METEO_DIR = "/mnt/meteo"

# prefix in regex format
METEO_PREFIX = "EN*"

# Test if dir exists
if os.path.isdir(METEO_DIR):
  os.chdir(METEO_DIR)
else:
  print("\nDirectory does not exist.")
  sys.exit()

# Load all files and sort as in AVAILABLE
meteo_files = glob.glob('EN*')
meteo_files.sort()

# Check if any meteo file in dir
if not meteo_files:
  print("\nDirectory does not contain meteo files.")
  sys.exit()

AVAILABLE = open('AVAILABLE', 'w')
AVAILABLE.write("-\n-\n-\n")

for meteo_file in meteo_files:
	# Sample line format "20130802 000000      EN13080200"
	AVAILABLE.write("20%s %s0000      %s\n" % (meteo_file[3:9], meteo_file[9:11], meteo_file))

AVAILABLE.close()

print("AVAILABLE file created in %s.\nPress Enter to exit." % METEO_DIR)
raw_input()