import os
# import re
import pandas as pd
import sqlite3

from datetime import date
from pandas.tseries.offsets import Week
from shutil import copy



def make_local_copy(config):
    chrome_history_file = os.path.expanduser(config['chrome_history_file'])
    history_file_local_copy = os.path.join(config['data_directory'], 'chrome_history')

    if not os.path.exists(config['data_directory']):
        os.mkdir(config['data_directory'])

    if (not os.path.exists(history_file_local_copy)
            or date.fromtimestamp(os.path.getmtime(history_file_local_copy)) < date.today()):
        copy(chrome_history_file, history_file_local_copy)


def windows_epoch_to_datetime(win_epoch):
    windows_to_unix_epoch_microseconds = 11644473600000000
    return pd.to_datetime(win_epoch - windows_to_unix_epoch_microseconds, unit='us')


def get_urls(config):
    urls = pd.read_sql(
        'select * from urls order by last_visit_time desc',
        con=sqlite3.connect(os.path.join(config['data_directory'], 'chrome_history')),
        index_col='id')

    urls.sort_values('visit_count', ascending=False, inplace=True)
    urls = urls[urls['visit_count'] > 0]

    # Convert last_visit_time

    urls['last_visit_time'] = windows_epoch_to_datetime(urls['last_visit_time'])

    # More cleanup here
    #  * Reduce size of data? Combine some rows based on cleaned up URLS?

    return urls


def get_visits(config):
    q = """select
               v.id as id
               ,u.url
               ,u.title
               ,v.visit_time
               ,v.transition
               ,v.visit_duration
               ,v.from_visit
               ,uf.url as from_url
               ,uf.title as from_title
             from visits v
             join urls u on u.id = v.url
             left join visits vf on vf.id=v.from_visit
             left join urls uf on uf.id=vf.url
             order by v.visit_time desc
    """

    visits = pd.read_sql(
        sql=q,
        con=sqlite3.connect(os.path.join(config['data_directory'], 'chrome_history')),
        index_col='id'
    )

    visits['visit_time'] = windows_epoch_to_datetime(visits['visit_time'])
    visits['visit_week'] = visits['visit_time'].apply(lambda x: Week(weekday=6, normalize=True).rollback(x))

    # https://developer.chrome.com/extensions/history#type-TransitionType
    transition_types = {
        0: 'link',
        1: 'typed',            # Typed into search bar (also auto-suggest from search bar)
        2: 'auto_bookmark',
        3: 'auto_subframe',    # Automatic navigation within a subframe
        4: 'manual_subframe',  # Navigation within a subframe
        5: 'generated',        # Did a search from the search bar, and chose an option)
        6: 'auto_toplevel',
        7: 'form_submit',
        8: 'reload',
        9: 'keyword',
        10: 'keyword_generated'
    }
    visits['transition'] = visits['transition'].apply(lambda x: transition_types[x & 0x000000FF])
    idx = visits.transition.isin(['reload', 'form_submit', 'auto_subframe', 'manual_subframe'])
    visits.drop(visits.index[idx], inplace=True)

    # Add a count of unique weeks visited by URL (for some reason to_numeric is needed to convert from a datetime)
    visits['weeks_observed'] = pd.to_numeric(visits.groupby('url')['visit_week'].transform('nunique'))

    return visits
