import datetime
import os
import platform
import yaml
import sqlalchemy
from warnings import warn
from shutil import copy

from custodial import metadata


if platform.system() != 'Darwin':
    raise NotImplementedError('Only Mac is supported at this time')

config_file = os.environ.get('CONFIG_FILE') or './config/custodial.yml'
with open(config_file, 'r') as ymlfile:
    try:
        config = yaml.load(ymlfile)
    except FileNotFoundError:
        config = {
            'application_data': 'sqlite:///data/custodial.sqlite3',
            'chrome_history_file': '~/Library/Application Support/Google/Chrome/Default/History',
            'data_directory': 'data'
        }

initial_config = config.copy()

print('Configuring Custodial:')
for key, value in config.items():
    newval = input("\t{} [{}]:".format(key, value))
    if newval:
        config[key] = newval
    if (key in ['chrome_history_file', 'data_directory']
            and not os.path.exists(os.path.expanduser(config[key]))):
        warn("The file/directory: '{}' does not exist.".format(config[key]))


if initial_config != config:
    copy(config_file, config_file + '.' + datetime.datetime.now().strftime('%Y%m%d%H%M'))
    with open(config_file, 'w') as ymlfile:
        yaml.dump(config, ymlfile, default_flow_style=False)

print('\nInitializing Application Database')
engine = sqlalchemy.create_engine(config['application_data'])
metadata.metadata.create_all(engine)
print('Done')
