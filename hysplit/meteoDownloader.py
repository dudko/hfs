#! /usr/bin/python2.7

""" Download GDAS data start ftp://arlftp.arlhq.noaa.gov/pub/archives/gdas1/
for specified date range. Can be used as a module or as a standalone program.
"""

""" Modules """
from ftplib import FTP
from datetime import date
import ftplib
import os

""" Constants """
START = (12, 2012)
END = (1, 2013)
OUTDIR = 'C:/out'

MONTHS = [
    'jan', 'feb', 'mar', 'apr',
    'may', 'jun', 'jul', 'aug',
    'sep', 'oct', 'nov', 'dec'
]

FTPADDR = 'arlftp.arlhq.noaa.gov'
WORKDIR = 'pub/archives/gdas1'

""" Functions """
def downloadMeteo(start, end, outdir):
    """
    Download meteo files for a given date range.
    """
    # Create output dir if not exists
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    # Set date objects
    start_date = date(start[1], start[0], 1)
    end_date= date(end[1], end[0], 1)

    months_delta = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month) + 1 #
    current_year = start_date.year
    current_month = start_date.month - 1

    # Load all months
    months_all = []

    for i in range(months_delta):
        months_all.append(str(MONTHS[current_month]) + str(current_year)[2:4])
        if current_month == 11:
            current_month = 0
            current_year += 1
        else:
            current_month += 1

    # Download data
    print "STARTING TO DOWNLOAD"

    ftp = FTP(FTPADDR)
    ftp.login ()
    ftp.cwd(WORKDIR)
    os.chdir(outdir)

    for i in months_all:
        for j in range(1, 6):
            filename = "gdas1." + i + ".w" + str(j)
            print "* " + filename
            output_file = open(filename, 'wb')

            try:
                ftp.retrbinary("RETR %s" % filename, output_file.write)
            except ftplib.all_errors:
                print "File \"%s\" does not exists." % filename

            output_file.close()

""" Run standalone """
if __name__ == '__main__':
    downloadMeteo(START, END, OUTDIR)
