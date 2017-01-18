import pandas as pd
import pytest

from mock import Mock
from urllib.parse import urlparse

from custodial import bookmarks


@pytest.fixture
def candidates(visits):
    aggregation = {
        'visit_week': {
            'visit_count': 'count',
            'first_week_observed': 'min',
            'latest_week_observed': 'max'
        }
    }

    candidates = visits[visits.weeks_observed >= 3].groupby(['url', 'weeks_observed'], as_index=False).agg(aggregation)
    candidates.columns = ['url', 'weeks_observed', 'first_week_observed', 'latest_week_observed', 'visit_count']
    return candidates


@pytest.fixture
def hostnames():
    return pd.Series(['docs.google.com', 'acme.com'])


excluded_hostnames = Mock(return_value=['docs.google.com'])


def test_identify_bookmark_exclusions_fails_when_its_argument_is_not_a_series():
    with pytest.raises(TypeError):
        bookmarks.identify_bookmark_exclusions(['This', 'is a list', 'not a series'])


def test_identify_bookmark_exclusions_removes_hostnames_in_bookmark_exclusions(hostnames):
    exclusions = bookmarks.identify_bookmark_exclusions(hostnames)
    assert set([hostnames[i] for i in exclusions]).issubset(set(excluded_hostnames()))


def test_filter_bookmark_candidates_contains_only_valid_schemes(candidates):
    cd = bookmarks.filter_bookmark_candidates(candidates)
    schemes = cd.url.apply(lambda u: urlparse(u).scheme)

    assert set(schemes.unique()).issubset(set(bookmarks.VALID_SCHEMES))


def test_filter_bookmark_candidates_removes_excluded_hostnames(candidates):
    cd = bookmarks.filter_bookmark_candidates(candidates)
    hostnames = cd.url.apply(lambda u: urlparse(u).hostname)

    assert set(hostnames.unique()).isdisjoint(set(excluded_hostnames()))
