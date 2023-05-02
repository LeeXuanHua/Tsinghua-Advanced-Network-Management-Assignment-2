import pandas as pd
import numpy as np
import glob

from typing import List


# Read Host Data
def read_host(prefix_path: str = "test_data", 
              filename_pattern: str = "*", 
              verbose: bool = False) -> pd.DataFrame:
    """
    Using the filename pattern specified (e.g. 'os_linux' or '*'), read all the host data into a single dataframe.

    dtype mapping is specified to reduce memory usage.
    """
    # For test_data, the memory usage is maintained at around 52.5+ MB.
    host_dtype_mapping = {
        'itemid': np.uint64,
        'name': 'category',
        'bomc_id': 'category',
        'timestamp': np.uint64,
        'value': 'float64',
        'cmdb_id': 'category',
    }

    host_pattern = f"data/{prefix_path}/host/{filename_pattern}.csv"

    # Combine all the files into 1 dataframe
    host_df = pd.concat([pd.read_csv(file, dtype=host_dtype_mapping) for file in glob.glob(host_pattern)], ignore_index=True)

    # Convert timestamps to datetime64[ns, Asia/Singapore] via vectorized operation
    # For test_data, no change in memory (52.5+ MB)
    host_df['timestamp'] = pd.to_datetime(host_df['timestamp'], unit='ms', utc=True).dt.tz_convert('Asia/Singapore')

    if verbose:
        print("The host dataframe has %s rows and %s columns" % host_df.shape)
        print("\nSummary info of host dataframe:")
        host_df.info()

    return host_df


# Read Trace Data
def read_trace(prefix_path: str = "test_data", 
              filename_pattern: str = "*", 
              verbose: bool = False,
              test_data: bool = False) -> pd.DataFrame:
    """
    Using the filename pattern specified (e.g. 'trace_fly_remote' or '*'), read all the trace data into a single dataframe.

    dtype mapping is specified to reduce memory usage.
    """
    # For test_data, the memory usage reduces from 1.5+ GB (default) to 1.4+ GB
    trace_dtype_mapping = {
        'callType': 'category',
        'startTime': np.uint64,
        'elapsedTime': np.uint32,
        'success': bool,
        'traceId': 'category',
        'id': 'object',
        'pid': 'category',
        'cmdb_id': 'category',
        'serviceName': 'category'
    }

    # If data is test_data, add msgTime column (Note that train_data does not have msgTime column)
    if test_data: trace_dtype_mapping.update({'msgTime': np.uint64}) 

    trace_data_pattern = f"data/{prefix_path}/trace/{filename_pattern}.csv"

    # Combine all the files into 1 dataframe
    trace_df = pd.concat([pd.read_csv(file, dtype=trace_dtype_mapping) for file in glob.glob(trace_data_pattern)], ignore_index=True)

    # Convert timestamps to datetime64[ns, Asia/Singapore] via vectorized operation
    # For test_data, no noticeable change in memory (1.4+ GB)
    trace_df.elapsedTime = trace_df.elapsedTime.astype(np.int16)
    trace_df.startTime = pd.to_datetime(trace_df.startTime, unit='ms', utc=True).dt.tz_convert('Asia/Singapore')
    if test_data: trace_df.msgTime = pd.to_datetime(trace_df.msgTime, unit='ms', utc=True).dt.tz_convert('Asia/Singapore')

    if verbose:
        print("The trace dataframe has %s rows and %s columns" % trace_df.shape)
        print("\nSummary info of trace dataframe:")
        trace_df.info()

    return trace_df


# Read ESB Data
def read_esb(esb_filepath, verbose=False):
    """
    Using the filepath specified, read the ESB data into a single dataframe.

    dtype mapping is specified to reduce memory usage.
    """
    # For test_data, the memory usage reduces from 33.9+ KB (default) to 20.5 KB
    esb_dtype_mapping = {
        'serviceName': 'category',
        'startTime': np.uint64,
        'avg_time': np.float64,
        'num': np.uint16,
        'succee_num': np.uint16,
        'succee_rate': np.float64,
    }

    # Combine all the files into 1 dataframe
    esb_df = pd.concat([pd.read_csv(file, dtype=esb_dtype_mapping) for file in glob.glob(esb_filepath)], ignore_index=True)

    # Convert timestamps to datetime64[ns, Asia/Singapore] via vectorized operation
    # For test_data, no noticeable change in memory (20.5 KB)
    esb_df.startTime = pd.to_datetime(esb_df.startTime, unit='ms', utc=True).dt.tz_convert('Asia/Singapore')

    if verbose:
        print("The ESB dataframe has %s rows and %s columns" % esb_df.shape)
        print("Summary info of ESB dataframe:\n" + esb_df.info())
        esb_df.head(5)

        print("The ESB dataframe has %s rows and %s columns" % esb_df.shape)
        print("\nSummary info of ESB dataframe:")
        esb_df.info()
        
    return esb_df


# Calculate Trace Length
def trace_length(df: pd.DataFrame, trace_list: List[str]) -> List[int]:
    """
    Query the dataframe to obtain each trace and return their length.

    This is helpful to determine if the failure resulted in a longer (e.g. calling alternative services for error handling) 
    or shorter (e.g. skipping certain calls through error handling) trace.
    """
    trace_length_list = []

    for trace in trace_list:
        trace_length_list.append(len(df[df.traceId == trace]))

    return trace_length_list