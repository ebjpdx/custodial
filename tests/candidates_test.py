import pandas as pd
import pytest

from mock import Mock
from urllib.parse import urlparse

from custodial import candidates


@pytest.fixture
def cnd(visits):
    aggregation = {
        'visit_week': {
            'visit_count': 'count',
            'first_week_observed': 'min',
            'latest_week_observed': 'max'
        }
    }

    cnd = visits[visits.weeks_observed >= 3].groupby(['url', 'weeks_observed'], as_index=False).agg(aggregation)
    cnd.columns = ['url', 'weeks_observed', 'first_week_observed', 'latest_week_observed', 'visit_count']
    return cnd


@pytest.fixture
def hostnames():
    return pd.Series(['docs.google.com', 'acme.com'])


excluded_hostnames = Mock(return_value=['docs.google.com'])


def test_identify_url_exclusions_fails_when_its_argument_is_not_a_series():
    with pytest.raises(TypeError):
        candidates.identify_url_exclusions(['This', 'is a list', 'not a series'])


def test_identify_url_exclusions_removes_hostnames_in_bookmark_exclusions(hostnames):
    exclusions = candidates.identify_url_exclusions(hostnames)
    assert set([hostnames[i] for i in exclusions]).issubset(set(excluded_hostnames()))


def test_filter_urls_contains_only_valid_schemes(cnd):
    cd = candidates.filter_urls(cnd)
    schemes = cd.url.apply(lambda u: urlparse(u).scheme)

    assert set(schemes.unique()).issubset(set(candidates.VALID_SCHEMES))


def test_filter_urls_removes_excluded_hostnames(cnd):
    cd = candidates.filter_urls(cnd)
    hostnames = cd.url.apply(lambda u: urlparse(u).hostname)

    assert set(hostnames.unique()).isdisjoint(set(excluded_hostnames()))


def test_get_fails_when_method_does_not_return_a_data_frame():
    with pytest.raises(TypeError):
        candidates.get(lambda x: list(range(0, 10)))


def test_get_fails_when_candidates_does_not_have_a_column_called_url():
    with pytest.raises(TypeError):
        candidates.get(lambda: pd.DataFrame({'not_url': ['a','b','c','d'], 'first_week_observed': ['a','b','c','d'], 'latest_week_observed': ['a','b','c','d']}))


def test_get_fails_when_candidates_does_not_have_a_column_called_first_week_observed():
    with pytest.raises(TypeError):
        candidates.get(lambda: pd.DataFrame({'url': ['a','b','c','d'], 'not_first_week_observed': ['a','b','c','d'], 'latest_week_observed': ['a','b','c','d']}))


def test_get_fails_when_candidates_does_not_have_a_column_called_last_week_observed():
    with pytest.raises(TypeError):
        candidates.get(lambda: pd.DataFrame({'url': ['a','b','c','d'], 'first_week_observed': ['a','b','c','d'], 'not_latest_week_observed': ['a','b','c','d']}))
