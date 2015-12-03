## Batch processing for HYSPLIT

Run HYSPLITs trajectory model in batch using run definitions from CSV file. The  idea is to run the model for each given hour every day within the date range.

#### Requirements

* >= Python 2.7
* latest version of HYSPLIT
* spatial analysis requires >= ArcMap v.10

#### Defining runs

Runs executed in batch are defined in CSV file. This file must have the format as in [`sample_runs.csv`](https://github.com/dudko/hfs/blob/master/hysplit/sample_runs.csv). CSV files can be prepared and further updated by major spreadsheet editors.

The direction of the run goes forward with positive value for runtime hours and backwards with negative one.