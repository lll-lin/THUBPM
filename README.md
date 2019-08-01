# sudden drifts detection
Detecting process drift from event log.
## Python packages required
- lxml (http://lxml.de/)
- numpy (http://www.numpy.org/)


## How to use **************************************************
Command line usage:
```
python driftDetection.py [-w value] [-r value] [-p value] log_file_path
options:
    -w complete window size, integer, default value is 200
    -r detection window size, integer, default value is 200
    -p stable period, integer, default value is 10
```
Examples:
```
 python driftDetection.py -w 200 -r 200 -p 10 log/IRO10k.mxml
 python driftDetection.py  log/IRO10k.mxml
```

Note: if you have 'Error reading file ', please using absolute path of log file.


## A reference for users **************************************************
Many algorithms always suffer the problem with how to set the parameters.
In our paper, we presented two equations (i.e., ML and LCE) to provide a reference for users with improving the accuracy of their detecion.

If you want to learn more about log completeness, you can read our previous works:
(1)An Approach to Evaluate the Local Completeness of an Event Log
(2)Estimating Global Completeness of Event Logs: A Comparative Study


## Thanks **************************************************
Test data is provided by A. Maaradji, M. Dumas, M. La Rosa and A. Ostovar etc.