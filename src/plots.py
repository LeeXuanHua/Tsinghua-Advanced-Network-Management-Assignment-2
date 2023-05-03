import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

from typing import Tuple

from .utils import read_esb, trace_length


# Analyse & Compare 2 ESB graphs
def compare_esb(seconds_past: int, 
                interval: int = 60, 
                test_esb_filepath: str = r"data/test_data/esb.csv", 
                train_esb_filepath: str = r"data/train_data/2020_05_04/esb.csv") -> Tuple[pd.DataFrame, pd.DataFrame]:
      '''
      Since ESB data are recorded in intervals of 1 min, we filter the data by to the specified range (in mins) around the timestamp.

      Beware of the interval choice to avoid error (empty graph) due to missing data.
      E.g. For 00:37:00, if interval = 80, there is no data earlier than 00:00:00
      '''
      # Return hh:mm:ss from seconds
      hh_mm_ss_dt = pd.to_datetime(seconds_past, unit='s')
      hh_mm_ss_str = hh_mm_ss_dt.time().strftime('%H:%M:%S')


      test_esb = read_esb(test_esb_filepath)
      train_esb = read_esb(train_esb_filepath)

      # Filter by timestamp range
      test_esb.startTime = test_esb.startTime.dt.time
      train_esb.startTime = train_esb.startTime.dt.time

      test_esb = test_esb[
            (test_esb.startTime >= (hh_mm_ss_dt - pd.Timedelta(minutes=interval/2)).time()) & 
            (test_esb.startTime <= (hh_mm_ss_dt + pd.Timedelta(minutes=interval/2)).time())]
      train_esb = train_esb[
            (train_esb.startTime >= (hh_mm_ss_dt - pd.Timedelta(minutes=interval/2)).time()) & 
            (train_esb.startTime <= (hh_mm_ss_dt + pd.Timedelta(minutes=interval/2)).time())]


      # Plot the data
      fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(30, 15))
      plt.setp(ax1.xaxis.get_majorticklabels(), rotation=90)
      plt.setp(ax2.xaxis.get_majorticklabels(), rotation=90)
      plt.setp(ax3.xaxis.get_majorticklabels(), rotation=90)
      plt.setp(ax4.xaxis.get_majorticklabels(), rotation=90)

      test_dates = [datetime.datetime.strptime(str(ts), '%H:%M:%S') for ts in test_esb.startTime]
      train_dates = [datetime.datetime.strptime(str(ts), '%H:%M:%S') for ts in train_esb.startTime]

      # Plot avg_time & add a vertical line at x = 0.5
      ax1.plot(test_dates, test_esb.avg_time, label='avg_time (test)')
      ax1.plot(train_dates, train_esb.avg_time, label='avg_time (train)', color='orange', alpha=0.5)
      ax1.axvline(x=datetime.datetime.strptime(hh_mm_ss_str, '%H:%M:%S'), color='r', linestyle='--', label=hh_mm_ss_str)
      try:
            ax1.fill_between(test_dates, test_esb.avg_time, train_esb.avg_time, color='blue', alpha=0.05)
      except:
            pass

      ax1.set_title('avg_time', fontsize=15, fontweight='bold', pad=30, color='black', loc='center')
      ax1.set_xlabel('timestamp')
      ax1.set_ylabel('avg_time (ms)')
      # ax1.xaxis.set_major_locator(mdates.MinuteLocator(interval=5))
      ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
      ax1.legend(loc='upper left')

      # Plot num & add a vertical line at x = 0.5
      ax2.plot(test_dates, test_esb.num, label='num (test)')
      ax2.plot(train_dates, train_esb.num, label='num (train)', color='orange', alpha=0.5)
      ax2.axvline(x=datetime.datetime.strptime(hh_mm_ss_str, '%H:%M:%S'), color='r', linestyle='--', label=hh_mm_ss_str)
      try:
            ax2.fill_between(test_dates, test_esb.num, train_esb.num, color='blue', alpha=0.05)
      except:
            pass

      ax2.set_title('num', fontsize=15, fontweight='bold', pad=30, color='black', loc='center')
      ax2.set_xlabel('timestamp')
      ax2.set_ylabel('num')
      # ax2.xaxis.set_major_locator(mdates.MinuteLocator(interval=5))
      ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
      ax2.legend(loc='upper left')

      # Plot succee_num & add a vertical line at x = 0.5
      ax3.plot(test_dates, test_esb.succee_num, label='succee_num (test)')
      ax3.plot(train_dates, train_esb.succee_num, label='succee_num (train)', color='orange', alpha=0.5)
      ax3.axvline(x=datetime.datetime.strptime(hh_mm_ss_str, '%H:%M:%S'), color='r', linestyle='--', label=hh_mm_ss_str)
      try:
            ax3.fill_between(test_dates, test_esb.succee_num, train_esb.succee_num, color='blue', alpha=0.05)
      except:
            pass

      ax3.set_title('succee_num', fontsize=15, fontweight='bold', pad=30, color='black', loc='center')
      ax3.set_xlabel('timestamp')
      ax3.set_ylabel('succee_num')
      # ax3.xaxis.set_major_locator(mdates.MinuteLocator(interval=5))
      ax3.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
      ax3.legend(loc='upper left')

      # Plot succee_rate & add a vertical line at x = 0.5
      ax4.plot(test_dates, test_esb.succee_rate, label='succee_rate (test)')
      ax4.plot(train_dates, train_esb.succee_rate, label='succee_rate (train)', color='orange', alpha=0.5)
      ax4.axvline(x=datetime.datetime.strptime(hh_mm_ss_str, '%H:%M:%S'), color='r', linestyle='--', label=hh_mm_ss_str)
      try:
            ax4.fill_between(test_dates, test_esb.succee_rate, train_esb.succee_rate, color='blue', alpha=0.05)
      except:
            pass

      ax4.set_title('succee_rate', fontsize=15, fontweight='bold', pad=30, color='black', loc='center')
      ax4.set_xlabel('timestamp')
      ax4.set_ylabel('succee_rate')
      # ax4.xaxis.set_major_locator(mdates.MinuteLocator(interval=5))
      ax4.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
      ax4.legend(loc='upper left')

      # Add a title for the entire plot
      fig.suptitle(f'Comparing ESB Data at {hh_mm_ss_str} (Range: {interval} mins)', fontsize=20, fontweight='bold', color='red', x=0.5)
      plt.tight_layout()
      plt.show()

      return test_esb, train_esb


# Analyse & Compare 2 Host graphs
def compare_host(test_host: pd.DataFrame, 
                train_host: pd.DataFrame,
                seconds_past: int,
                cmdb_id: str,
                name: str,
                interval: int = 60) -> Tuple[pd.DataFrame, pd.DataFrame]:
      '''
      The data will first be filtered based on cmdb_id and name/key_name.

      Since host data KPIs are recorded in different intervals (some in 1 second interval, some in 5 min interval), we filter the data by to the specified range (in seconds for greater granularity) around the timestamp.

      Beware of the interval choice to avoid error (empty graph) due to missing data.
      E.g. For 00:37:00, if interval = 80, there is no data earlier than 00:00:00
      '''
      # Return hh:mm:ss from seconds
      hh_mm_ss_dt = pd.to_datetime(seconds_past, unit='s')
      hh_mm_ss_str = hh_mm_ss_dt.time().strftime('%H:%M:%S')


      # Filter based on cmdb_id and name
      test_host = test_host[(test_host.cmdb_id == cmdb_id) & (test_host.name == name)]
      train_host = train_host[(train_host.cmdb_id == cmdb_id) & (train_host.name == name)]

      # Filter by timestamp range
      test_host.timestamp = test_host.timestamp.dt.time
      train_host.timestamp = train_host.timestamp.dt.time

      test_host = test_host[
            (test_host.timestamp >= (hh_mm_ss_dt - pd.Timedelta(seconds=interval/2)).time()) & 
            (test_host.timestamp <= (hh_mm_ss_dt + pd.Timedelta(seconds=interval/2)).time())]
      train_host = train_host[
            (train_host.timestamp >= (hh_mm_ss_dt - pd.Timedelta(seconds=interval/2)).time()) & 
            (train_host.timestamp <= (hh_mm_ss_dt + pd.Timedelta(seconds=interval/2)).time())]

      # # Truncate the 2 dataframe to the same length
      # train_host = train_host.iloc[:len(test_host)]

      # Plot the data
      fig, ax = plt.subplots(1, 1, figsize=(30, 15))
      plt.setp(ax.xaxis.get_majorticklabels(), rotation=90)

      test_dates = [datetime.datetime.strptime(str(ts), '%H:%M:%S') for ts in test_host.timestamp]
      train_dates = [datetime.datetime.strptime(str(ts), '%H:%M:%S') for ts in train_host.timestamp]

      # Plot avg_time & add a vertical line at x = 0.5
      ax.plot(test_dates, test_host.value, label=f'{name} value (test)')
      ax.plot(train_dates, train_host.value, label=f'{name} value (train)', color='orange', alpha=0.5)
      ax.axvline(x=datetime.datetime.strptime(hh_mm_ss_str, '%H:%M:%S'), color='r', linestyle='--', label=hh_mm_ss_str)
      try:
            ax.fill_between(test_dates, test_host.value, train_host.value, color='blue', alpha=0.05)
      except:
            pass

      ax.set_title(name, fontsize=15, fontweight='bold', pad=30, color='black', loc='center')
      ax.set_xlabel('timestamp')
      ax.set_ylabel(name)
      # ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=5))
      ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
      ax.legend(loc='upper left')

      # Add a title for the entire plot
      fig.suptitle(f'Comparing Host Data for {cmdb_id} at {hh_mm_ss_str} (Range: {interval} seconds)', fontsize=20, fontweight='bold', color='red', x=0.5)
      plt.tight_layout()
      plt.show()

      return test_host, train_host

# Analyse & Compare 2 Trace graphs for Failure 1
def compare_trace_for_failure(test_trace: pd.DataFrame, 
                                train_trace: pd.DataFrame,
                                seconds_past: int,
                                interval: int = -1, 
                                # strictly_parent: bool = True
                              ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
      '''
      # Depending on the value of strictly_parent, the data will first be filtered based pid == 'None' for strictly_parent rows.

      This allows us to obtain the parent traceId and compare the data of the parent traceId.

      We filter the data to the specified range (in seconds for greater granularity) around the timestamp.

      Beware of the interval choice to avoid error (empty graph) due to missing data.
      E.g. For 00:37:00, if interval = 80, there is no data earlier than 00:00:00
      '''
      # Return hh:mm:ss from seconds
      hh_mm_ss_dt = pd.to_datetime(seconds_past, unit='s')
      hh_mm_ss_str = hh_mm_ss_dt.time().strftime('%H:%M:%S')

      # Dynamic interval (in seconds) to observe trend (same value used for both test and train)
      if interval == -1: interval = 3 * 2 * (test_trace.elapsedTime.max() / 100)   # Multiply by 3 again to observe the wider trend

      # Filter for start_time
      test_trace_filtered = test_trace[
            (test_trace.startTime.dt.time >= (hh_mm_ss_dt - pd.Timedelta(seconds=interval/2)).time()) & 
            (test_trace.startTime.dt.time <= (hh_mm_ss_dt + pd.Timedelta(seconds=interval/2)).time())]
      train_trace_filtered = train_trace[
            (train_trace.startTime.dt.time >= (hh_mm_ss_dt - pd.Timedelta(seconds=interval/2)).time()) &
            (train_trace.startTime.dt.time <= (hh_mm_ss_dt + pd.Timedelta(seconds=interval/2)).time())]

      # Filter for parent rows only
      test_trace_filtered_parent = test_trace_filtered[test_trace_filtered.pid == 'None']
      train_trace_filtered_parent = train_trace_filtered[train_trace_filtered.pid == 'None']

      # Sample 100 parent traceId
      test_trace_sampled_parent = test_trace_filtered_parent.sample(100).sort_values(by='startTime')
      train_trace_sampled_parent = train_trace_filtered_parent.sample(100).sort_values(by='startTime')

      # Obtain the parent traceId
      test_parent_traceId_list = test_trace_sampled_parent.traceId.tolist()
      train_parent_traceId_list = train_trace_sampled_parent.traceId.tolist()

      # Obtain traceId length
      test_trace_length_list = trace_length(test_trace, test_parent_traceId_list)
      train_trace_length_list = trace_length(train_trace, train_parent_traceId_list)

      # Create the timestamps for graph axis
      test_dates = []
      for ts in test_trace_sampled_parent.startTime.dt.time:
            try:
                  test_dates.append(datetime.datetime.strptime(str(ts), '%H:%M:%S.%f'))
            except:
                  test_dates.append(datetime.datetime.strptime(str(ts), '%H:%M:%S'))

      train_dates = []
      for ts in train_trace_sampled_parent.startTime.dt.time:
            try:
                  train_dates.append(datetime.datetime.strptime(str(ts), '%H:%M:%S.%f'))
            except:
                  train_dates.append(datetime.datetime.strptime(str(ts), '%H:%M:%S'))


      # Graph 1: traceId length
      # Graph 2: elapsedTime (parent - os_021)
      # Graph 3: elapsedTime (parent - os_022)

      # Graph 1: traceId length
      fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(30, 15))

      # Plot avg_time & add a vertical line at x = 0.5
      ax1.plot(test_dates, test_trace_length_list, label='os_021 trace length (test)')
      ax1.plot(train_dates, train_trace_length_list, label='os_021 trace length (train)', color='orange', alpha=0.5)
      ax1.axvline(x=datetime.datetime.strptime(hh_mm_ss_str, '%H:%M:%S'), color='r', linestyle='--', label=hh_mm_ss_str)

      ax1.set_title("Trace Length", fontsize=15, fontweight='bold', pad=30, color='black', loc='center')
      ax1.set_xlabel('timestamp')
      ax1.set_ylabel('trace length')
      # ax1.xaxis.set_major_locator(mdates.MinuteLocator(interval=5))
      ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
      ax1.legend(loc='upper left')


      # Graph 2: elapsedTime (parent - os_021)
      # Create the timestamps for graph axis
      name = 'os_021'
      test_trace_filtered_parent_os_021 = test_trace_filtered_parent[test_trace_filtered_parent.cmdb_id == name]
      train_trace_filtered_parent_os_021 = train_trace_filtered_parent[train_trace_filtered_parent.cmdb_id == name]

      test_dates = []
      for ts in test_trace_filtered_parent_os_021.startTime.dt.time:
            try:
                  test_dates.append(datetime.datetime.strptime(str(ts), '%H:%M:%S.%f'))
            except:
                  test_dates.append(datetime.datetime.strptime(str(ts), '%H:%M:%S'))

      train_dates = []
      for ts in train_trace_filtered_parent_os_021.startTime.dt.time:
            try:
                  train_dates.append(datetime.datetime.strptime(str(ts), '%H:%M:%S.%f'))
            except:
                  train_dates.append(datetime.datetime.strptime(str(ts), '%H:%M:%S'))

      # Plot elapsedTime for os_021 & add a vertical line at x = 0.5
      ax2.plot(test_dates, test_trace_filtered_parent_os_021.elapsedTime, label=f'{name} elapsedTime (test)')
      ax2.plot(train_dates, train_trace_filtered_parent_os_021.elapsedTime, label=f'{name} elapsedTime (train)', color='orange', alpha=0.5)
      ax2.axvline(x=datetime.datetime.strptime(hh_mm_ss_str, '%H:%M:%S'), color='r', linestyle='--', label=hh_mm_ss_str)

      ax2.set_title(name, fontsize=15, fontweight='bold', pad=30, color='black', loc='center')
      ax2.set_xlabel('timestamp')
      ax2.set_ylabel('elapsedTime')
      # ax2.xaxis.set_major_locator(mdates.MinuteLocator(interval=5))
      ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
      ax2.legend(loc='upper left')

      # Graph 3: elapsedTime (parent - os_022)
      # Create the timestamps for graph axis
      name = 'os_022'
      test_trace_filtered_parent_os_022 = test_trace_filtered_parent[test_trace_filtered_parent.cmdb_id == name]
      train_trace_filtered_parent_os_022 = train_trace_filtered_parent[train_trace_filtered_parent.cmdb_id == name]

      test_dates = []
      for ts in test_trace_filtered_parent_os_022.startTime.dt.time:
            try:
                  test_dates.append(datetime.datetime.strptime(str(ts), '%H:%M:%S.%f'))
            except:
                  test_dates.append(datetime.datetime.strptime(str(ts), '%H:%M:%S'))

      train_dates = []
      for ts in train_trace_filtered_parent_os_022.startTime.dt.time:
            try:
                  train_dates.append(datetime.datetime.strptime(str(ts), '%H:%M:%S.%f'))
            except:
                  train_dates.append(datetime.datetime.strptime(str(ts), '%H:%M:%S'))

      # Plot elapsedTime for os_022 & add a vertical line at x = 0.5
      ax3.plot(test_dates, test_trace_filtered_parent_os_022.elapsedTime, label=f'{name} elapsedTime (test)')
      ax3.plot(train_dates, train_trace_filtered_parent_os_022.elapsedTime, label=f'{name} elapsedTime (train)', color='orange', alpha=0.5)
      ax3.axvline(x=datetime.datetime.strptime(hh_mm_ss_str, '%H:%M:%S'), color='r', linestyle='--', label=hh_mm_ss_str)

      ax3.set_title(name, fontsize=15, fontweight='bold', pad=30, color='black', loc='center')
      ax3.set_xlabel('timestamp')
      ax3.set_ylabel('elapsedTime')
      # ax3.xaxis.set_major_locator(mdates.MinuteLocator(interval=5))
      ax3.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
      ax3.legend(loc='upper left')

      # Add a title for the entire plot
      fig.suptitle(f'Comparing Trace Data at {hh_mm_ss_str} (Range: {interval} seconds)', fontsize=20, fontweight='bold', color='red', x=0.5)
      plt.tight_layout()
      plt.show()

      return test_trace_filtered, train_trace_filtered, test_trace_length_list, train_trace_length_list,test_trace_filtered_parent_os_021, train_trace_filtered_parent_os_021, test_trace_filtered_parent_os_022, train_trace_filtered_parent_os_022

