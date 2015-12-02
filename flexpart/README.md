## Batch running of FLEXPART

Preparation of simulation for FLEXPART requires adjusting couple of configuration files and providing meteo data in supported format. Scripts available in this repository can simplify some of those tasks and allow batch execution.

### Requirements

* >= Python 2.7
* FLEXPART 8.2.3, although newer versions of FLEXPART might work

### Usage

In general, constants in scripts have to be adjusted before script execution.

##### Defining runs

Runs executed in batch are defined in CSV file. This file must have the format as in [file](https://github.com/dudko/hfs/blob/master/flexpart/sample_run.csv). CSV files can be prepared and further updated by major spreadsheet editors.

##### [`generateAvailable.py`](https://github.com/dudko/hfs/blob/master/flexpart/generateAvailable.py)

Generate AVAILABLE file for meteo files in specified directory. Included meteo files are filtered with regular expression.

##### [`generateOutgrid.py`](https://github.com/dudko/hfs/blob/master/flexpart/generateOutgrid.py)

Generate custom OUTGRID. 

##### [`batchRunFlexpart.py`](https://github.com/dudko/hfs/blob/master/flexpart/batchRunFlexpart.py)

Iteratively load run definitions and create configuration files (`pathnames, RELEASES, COMMAND`) according to them. `RELEASES` and `COMMAND` are generated from templates in [file](https://github.com/dudko/hfs/blob/master/flexpart/templates.py).