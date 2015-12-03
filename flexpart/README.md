## Batch running of FLEXPART

Preparation of simulation for FLEXPART requires adjusting couple of configuration files and providing meteo data in supported format. Scripts available in this repository can simplify some of those tasks and allow batch execution.

#### Requirements

* >= Python 2.7
* FLEXPART 8.2.3, although newer versions of FLEXPART might work

#### Defining runs

Runs executed in batch are defined in CSV file. This file must have the format as in [`sample_runs.csv`](https://github.com/dudko/hfs/blob/master/flexpart/sample_runs.csv). CSV files can be prepared and further updated by major spreadsheet editors.

Number of particles for releases can be either a constant value or special value calculated from time range of particular release. This special values is formated as `VALUE PERMIN`, what means that, `VALUE` number of particles will be released per minute.