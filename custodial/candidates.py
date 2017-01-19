import sqlalchemy
import pandas as pd

from urllib.parse import urlparse

from custodial.config import conn
from custodial import metadata


VALID_SCHEMES = ['https', 'http']


def excluded_hostnames():
    s = (sqlalchemy.select([metadata.bookmark_exclusions.c.url_pattern])
         .where(metadata.bookmark_exclusions.c.pattern_type == 'hostname'))
    result = conn.execute(s)

    return [row[0] for row in result]


def identify_url_exclusions(hostnames):
    if not type(hostnames) is pd.core.series.Series:
        raise TypeError('Identify_url_exclusions takes a pandas Series as input')

    return hostnames[hostnames.isin(excluded_hostnames())].index


def filter_urls(candidates):
    schemes = candidates.url.apply(lambda u: urlparse(u).scheme)
    candidates = candidates[schemes.isin(VALID_SCHEMES)]

    hostnames = candidates.url.apply(lambda u: urlparse(u).hostname)
    candidates = candidates.drop(identify_url_exclusions(hostnames))

    return candidates


def validate(candidates):
    if (type(candidates) != pd.core.frame.DataFrame):
        raise TypeError('Candidate recommenders need to return a pandas data frame')
    for col in ['url', 'first_week_observed', 'latest_week_observed']:
        if (col not in candidates.columns):
            raise TypeError("Candidate recommendations should contain a column called '{}'.".format(col))


def get(method, **kwargs):
    candidates = method(**kwargs)
    validate(candidates)
    return filter_urls(candidates)
