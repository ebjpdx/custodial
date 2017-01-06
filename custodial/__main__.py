import os
import platform
import yaml
import sqlalchemy

from custodial import chrome_history, metadata


if platform.system() != 'Darwin':
    raise NotImplementedError('Only Mac is supported at this time')

config_file = os.environ.get('CONFIG_FILE') or './config/custodial.yml'
with open(config_file, 'r') as ymlfile:
    config = yaml.load(ymlfile)

engine = sqlalchemy.create_engine(config['application_data'])

chrome_history.make_local_copy(config)
urls = chrome_history.get_urls(config)
visits = chrome_history.get_visits(config)
# bookmarker.add(urls)

# Should I create classes, or remain functional?
