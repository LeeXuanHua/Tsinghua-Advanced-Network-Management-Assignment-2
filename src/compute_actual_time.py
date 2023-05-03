import pandas as pd

from typing import Tuple
from collections import defaultdict

# Calculate Actual Time

# Note that this functions are very very slow
# A potential speed up is to track by the traceId instead, this avoids computing for every single row, maintaining large df and dictionaries
def build_dictionary_graph(df: pd.DataFrame) -> Tuple[dict, dict]:
    '''
    Using a dictionary, build a graph to mimic the hierarchy of the service tree.

    Elapsed time is stored in a dictionary with key = id, value = elapsed time. This is more time efficient than searching dataframe.

    Children dictionary is a dictionary with key = parent id, value = list of children id. This handles nested childrens too.
    '''
    elapsed_time_dict = {}
    children_dict = defaultdict(list)

    for index, row in df.iterrows():
        # Store elapsed time in a dictionary
        elapsed_time_dict[row['id']] = float(row['elapsedTime'])

        # If pid is not null, add the id to the children dictionary
        if row['pid']:
            children_dict[row['pid']].append(row['id'])

        # Above approach is adopted since we cannot be 100% sure the parent always come before the children (in terms of row index)
        # E.g. logging data may be illaccurate when services are called in close successions

    return elapsed_time_dict, children_dict


def compute_actual_time(df: pd.DataFrame, elapsed_time_dict: dict, children_dict: dict) -> pd.DataFrame:
    # Initialize a new column to store actual time
    df['actual_time'] = 0

    # Iterate through the df again, instead of following the dictionary to avoid filtering the df
    for index, row in df.iterrows():
        children_cumulative_time = 0

        # If the id is not in the children dictionary, it must be a leaf node
        if row['id'] not in children_dict.keys():
            df.at[index, 'actual_time'] = row['elapsedTime']
            continue
        
        # If the id is in the children dictionary, it must be a parent node
        # Therefore, compute the cumulative time of all children
        for child in children_dict[row['id']]:
            children_cumulative_time += elapsed_time_dict[child]

        # Subtract the cumulative time of its children from its elapsed time to get the actual time
        # This is the time spent on the service itself, excluding the time spent on its children
        df.at[index, 'actual_time'] = row['elapsedTime'] - children_cumulative_time

    return df

def avg_actual_time(trace_filtered, sample_trace):
    cumulative= pd.DataFrame()

    for trace_id in sample_trace:
        # Gather all the rows for the traceId
        temp = trace_filtered[trace_filtered.traceId == trace_id]

        # Build the dictionary graph and compute the actual time for each node
        elapsed_time_dict, children_dict = build_dictionary_graph(temp)
        temp = compute_actual_time(temp, elapsed_time_dict, children_dict)

        # Concatenate cmdb_id, serviceName, dsName to create a unique identifier (even if there are null values)
        temp['unique_identifier'] = temp['cmdb_id'].astype(str) + ':' + temp['serviceName'].astype(str) + ':' + temp['dsName'].astype(str)
        temp = temp.groupby('unique_identifier').agg({'actual_time': 'sum'}).sort_values(by='unique_identifier').reset_index()
        
        # Combine b1 and b2 to get sum of actual_time
        cumulative = pd.concat([cumulative, temp]).groupby('unique_identifier').agg({'actual_time': 'sum'}).sort_values(by='unique_identifier').reset_index()

    cumulative.actual_time = cumulative.actual_time / len(sample_trace)
    
    return cumulative

def compare_trace_childrens_failure1(test_trace_filtered, train_trace_filtered, test_trace_filtered_parent_host, train_trace_filtered_parent_host):
    sample_trace_test = test_trace_filtered_parent_host[test_trace_filtered_parent_host.elapsedTime > 4000].sample(100).traceId.tolist()
    sample_trace_train = train_trace_filtered_parent_host[
        (train_trace_filtered_parent_host.elapsedTime < train_trace_filtered_parent_host.elapsedTime.mean()) &
        (train_trace_filtered_parent_host.elapsedTime > 0)].sample(100).traceId.tolist()
    
    cumulative_test = avg_actual_time(test_trace_filtered, sample_trace_test)
    cumulative_train = avg_actual_time(train_trace_filtered, sample_trace_train)

    # Merge the two dataframes
    cumulative_train = cumulative_train.rename(columns={'actual_time': 'train_actual_time'})
    cumulative_test = cumulative_test.rename(columns={'actual_time': 'test_actual_time'})
    cumulative_train_test = pd.merge(cumulative_train, cumulative_test, on='unique_identifier', how='outer')

    # Calculate the difference between train and test
    cumulative_train_test['difference'] = cumulative_train_test.train_actual_time - cumulative_train_test.test_actual_time

    cumulative_train_test.sort_values(by='difference', ascending=True, inplace=True)
    
    return cumulative_train_test


def trace_to_parent(df:pd.DataFrame, traceId: str) -> pd.DataFrame:
    '''
    Given a traceId, query the dataframe and return the parent traceId.
    '''

    return df[(df.traceId == traceId) & (df.pid == "None")]


def compare_trace_childrens_failure2(test_trace_filtered, train_trace_filtered, test_trace_filtered_parent_host, train_trace_filtered_parent_host):
    sample_trace_test = test_trace_filtered_parent_host[(test_trace_filtered_parent_host.elapsedTime > 4000) | (test_trace_filtered_parent_host.elapsedTime < 0)].sample(100).traceId.tolist()
    sample_trace_train = train_trace_filtered_parent_host[
        (train_trace_filtered_parent_host.elapsedTime < train_trace_filtered_parent_host.elapsedTime.mean()) & 
        (train_trace_filtered_parent_host.elapsedTime > 0)].sample(100).traceId.tolist()
    
    cumulative_test = avg_actual_time(test_trace_filtered, sample_trace_test)
    cumulative_train = avg_actual_time(train_trace_filtered, sample_trace_train)

    # Merge the two dataframes
    cumulative_train = cumulative_train.rename(columns={'actual_time': 'train_actual_time'})
    cumulative_test = cumulative_test.rename(columns={'actual_time': 'test_actual_time'})
    cumulative_train_test = pd.merge(cumulative_train, cumulative_test, on='unique_identifier', how='outer')

    # Calculate the difference between train and test
    cumulative_train_test['difference'] = cumulative_train_test.train_actual_time - cumulative_train_test.test_actual_time

    cumulative_train_test.sort_values(by='difference', ascending=True, inplace=True)
    
    return cumulative_train_test

def compare_trace_childrens_failure4(test_trace_filtered, train_trace_filtered, test_trace_filtered_parent_host, train_trace_filtered_parent_host):
    avg_elapsed_for_errorneous_calls = test_trace_filtered_parent_host[
    (test_trace_filtered_parent_host.startTime > pd.to_datetime('2020-05-30 04:29:00').tz_localize('Asia/Singapore')) &
    (test_trace_filtered_parent_host.startTime < pd.to_datetime('2020-05-30 04:30:00').tz_localize('Asia/Singapore'))].elapsedTime.mean()
    
    sample_trace_test = test_trace_filtered_parent_host[test_trace_filtered_parent_host.elapsedTime < avg_elapsed_for_errorneous_calls].sample(100).traceId.tolist()
    sample_trace_train = train_trace_filtered_parent_host[
        (train_trace_filtered_parent_host.elapsedTime < train_trace_filtered_parent_host.elapsedTime.mean()) & 
        (train_trace_filtered_parent_host.elapsedTime > avg_elapsed_for_errorneous_calls)].sample(100).traceId.tolist()
    
    cumulative_test = avg_actual_time(test_trace_filtered, sample_trace_test)
    cumulative_train = avg_actual_time(train_trace_filtered, sample_trace_train)

    # Merge the two dataframes
    cumulative_train = cumulative_train.rename(columns={'actual_time': 'train_actual_time'})
    cumulative_test = cumulative_test.rename(columns={'actual_time': 'test_actual_time'})
    cumulative_train_test = pd.merge(cumulative_train, cumulative_test, on='unique_identifier', how='outer')

    # Calculate the difference between train and test
    cumulative_train_test['difference'] = cumulative_train_test.train_actual_time - cumulative_train_test.test_actual_time

    cumulative_train_test.sort_values(by='difference', ascending=True, inplace=True)
    
    return cumulative_train_test