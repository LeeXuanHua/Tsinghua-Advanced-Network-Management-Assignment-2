# Tsinghua-Advanced-Network-Management-Assignment-2/data
This folder contains all the data used for the assignment.

> 🚧 Reminder
> 
> To obtain the following data (`train_data/` & `test_data/`), run this [script](../scripts/download_datasets.sh) from the [root directory](../) via `./scripts/download_datasets.sh`

### [train_data](./train_data/)
This folder contains 1-day of data during the normal period. In other words, this data does not contain failures. Our report will use this data for comparison against attributes/statistics during failure to understand the anomalies.

We may also understand this folder as "normal_data".

### [test_data](./test_data/)
This folder contains data where failures are known to have occured. Our report will be revolving around the root cause analysis for these failures.

We may also understand this folder as "investigation_data".


### [cmdb.xlsx](cmdb.xlsx)
This file contains the overview of the system structure, where the column "name" is deployed on the column "host".


### [failures.json](failures.json)
This file contains basic information on the 5 failure instances that we are suppose to investigate in `test_data/`.

Note that the integer is the failure time, measured in seconds past 00:00. On the other hand, timestamp used in the datasets are in milliseconds.