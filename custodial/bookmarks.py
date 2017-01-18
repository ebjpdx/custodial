import pandas as pd
import sqlalchemy

from urllib.parse import urlparse


from custodial.config import conn
from custodial import metadata

VALID_SCHEMES = ['https', 'http']


def excluded_hostnames():
    s = (sqlalchemy.select([metadata.bookmark_exclusions.c.url_pattern])
         .where(metadata.bookmark_exclusions.c.pattern_type == 'hostname'))
    result = conn.execute(s)

    return [row[0] for row in result]


def current():
    pd.read_sql(
        sql='select * from bookmarks',
        con=conn,
        index_col='id'
    )


def identify_bookmark_exclusions(hostnames):
    if not type(hostnames) is pd.core.series.Series:
        raise TypeError('Identify_bookmark_exclusions takes a pandas Series as input')

    return hostnames[hostnames.isin(excluded_hostnames())].index


def filter_bookmark_candidates(candidates):
    schemes = candidates.url.apply(lambda u: urlparse(u).scheme)
    hostnames = candidates.url.apply(lambda u: urlparse(u).hostname)

    candidates = candidates[schemes.isin(VALID_SCHEMES)]
    candidates = candidates.drop(identify_bookmark_exclusions(hostnames))

    return candidates

