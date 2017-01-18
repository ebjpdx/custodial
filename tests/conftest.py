import os
import sys
import pytest

from shutil import copy

# Make sure that the application source directory (this directory's parent) is
# on sys.path.

here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, here)

from custodial import chrome_history


@pytest.fixture(scope='module')
def config(tmpdir_factory):
    return dict(chrome_history_file=os.path.join(str(tmpdir_factory.getbasetemp()), 'system_history_file'),
                data_directory=os.path.join(str(tmpdir_factory.getbasetemp()), 'data')
                )


@pytest.fixture(scope='module')
def visits(config):
    if not os.path.exists(config['data_directory']):
        os.mkdir(config['data_directory'])

    copy(os.path.join('tests', 'fixtures', 'chrome_history_20161207'),
         os.path.join(config['data_directory'], 'chrome_history'))
    return chrome_history.get_visits(config)
