import os
import re
import sqlite3
from datetime import date, datetime, timedelta
from shutil import copy

import pandas as pd


def make_local_copy(config):
    chrome_history_file = os.path.expanduser(config['chrome_history_file'])
    history_file_local_copy = os.path.join(config['data_directory'], 'chrome_history')

    if not os.path.exists(config['data_directory']):
        os.mkdir(config['data_directory'])

    if (not os.path.exists(history_file_local_copy)
            or date.fromtimestamp(os.path.getmtime(history_file_local_copy)) < date.today()):
        copy(chrome_history_file, history_file_local_copy)


def get_urls(config):
    urls = pd.read_sql(
        'select * from urls order by last_visit_time desc',
        con=sqlite3.connect(os.path.join(config['data_directory'], 'chrome_history')),
        index_col='id')

    urls.sort_values('visit_count', ascending=False, inplace=True)
    urls = urls[urls['visit_count'] > 0]

    # Convert last_visit_time
    windows_to_unix_epoch_microseconds = 11644473600000000

    urls['last_visit_time'] = pd.to_datetime(urls['last_visit_time'] - windows_to_unix_epoch_microseconds, unit='us')

    # More cleanup here
    #  * Reduce size of data? Combine some rows based on cleaned up URLS?

    return urls
