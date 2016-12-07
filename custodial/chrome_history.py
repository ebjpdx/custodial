import os
from shutil import copy


def make_local_copy(config):
  chrome_history_file = os.path.expanduser(config['chrome_history_file'])
  history_file_local_copy = os.path.join(config['data_directory'],'chrome_history')

  if not os.path.exists(config['data_directory']):
      os.mkdir(config['data_directory'])

  if (not os.path.exists(history_file_local_copy)
        or date.fromtimestamp(os.path.getmtime(history_file_local_copy)) < date.today()
      ):
      copy(chrome_history_file,history_file_local_copy)


