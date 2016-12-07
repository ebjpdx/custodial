import pytest
from  os import path

from custodial import chrome_history

@pytest.fixture
def config(tmpdir_factory):
    return dict(chrome_history_file=path.join(str(tmpdir_factory.getbasetemp()),'system_history_file')
      ,data_directory=path.join(str(tmpdir_factory.getbasetemp()),'data')
      )

def test_make_local_copy_fails_when_file_does_not_exist(config):
    with pytest.raises(FileNotFoundError):
        chrome_history.make_local_copy(config)

def test_make_local_copy_works_when_a_copy_does_not_already_exist(config,tmpdir_factory):
    p = tmpdir_factory.getbasetemp().join("system_history_file")
    p.write('something')
    chrome_history.make_local_copy(config)
    assert path.isfile(path.join(config['data_directory'],'chrome_history'))
