import pandas as pd
import pytest
from os import path
from shutil import copy


from custodial import chrome_history


@pytest.fixture
def config(tmpdir_factory):
    return dict(chrome_history_file=path.join(str(tmpdir_factory.getbasetemp()), 'system_history_file'),
                data_directory=path.join(str(tmpdir_factory.getbasetemp()), 'data')
                )


@pytest.fixture
def urls(config):
    copy(path.join('tests', 'fixtures', 'chrome_history_20161207'),
         path.join(config['data_directory'], 'chrome_history'))
    return chrome_history.get_urls(config)


@pytest.fixture
def visits(config):
    copy(path.join('tests', 'fixtures', 'chrome_history_20161207'),
         path.join(config['data_directory'], 'chrome_history'))
    return chrome_history.get_visits(config)


def test_make_local_copy_fails_when_file_does_not_exist(config):
    with pytest.raises(FileNotFoundError):
        chrome_history.make_local_copy(config)


def test_make_local_copy_works_when_a_copy_does_not_already_exist(config, tmpdir_factory):
    p = tmpdir_factory.getbasetemp().join("system_history_file")
    p.write('something')
    chrome_history.make_local_copy(config)
    assert path.isfile(path.join(config['data_directory'], 'chrome_history'))


def test_get_urls_has_the_right_columns_and_types(urls):
    column_types = {
        'favicon_id': 'int64',
        'hidden': 'int64',
        'last_visit_time': 'datetime64[ns]',
        'title': 'object',
        'typed_count': 'int64',
        'url': 'object',
        'visit_count': 'int64'}

    dt = urls.dtypes.to_dict()
    assert dt == column_types


def test_get_urls_last_visit_time_values_are_reasonable(urls):
    assert min(urls['last_visit_time']) >= pd.to_datetime('2000')


def test_get_visits_has_the_right_columns_and_types(visits):
    column_types = {
        'url': 'object',
        'title': 'object',
        'visit_time': 'datetime64[ns]',
        'visit_week': 'datetime64[ns]',
        'transition': 'object',
        'visit_duration': 'int64',
        'from_visit': 'int64',
        'from_url': 'object',
        'from_title': 'object'
    }

    dt = visits.dtypes.to_dict()
    assert dt == column_types


def test_get_visits_last_visit_time_values_are_reasonable(visits):
    assert min(visits['visit_time']) >= pd.to_datetime('2000')


def test_get_visits_blacklisted_transitions_are_excluded(visits):
    assert visits.transition.isin(['reload', 'form_submit','auto_subframe','manual_subframe']).sum() == 0
