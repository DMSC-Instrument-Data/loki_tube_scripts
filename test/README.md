# LOKI FullDataReductionScript Test
This test is performed against data collected at ISIS on the LARMOUR beamline using two LOKI prototype modules. It does not currently account
for the entire LOKI geometry.

## Requirements
* [Mantid 5.0](https://download.mantidproject.org/) or above 
* The following python modules: 
  * `unittest`.
  * `numpy`.
  * `mantidpython` (will be part of the Mantid 5.0 package).


## Basic Instruction for running in terminal
* set `PYTHONPATH` environment variable to include `loki_tube_scripts` location. 
* `cd` to the location of this test file.
* Launch the script using `mantidpython` bash/shell script.


**NB** You could also make use of a python IDE like [Pycharm](https://www.jetbrains.com/pycharm/).
