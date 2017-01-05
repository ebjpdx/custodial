import platform
import yaml
import os


from custodial import chrome_history

# Only supported on mac right now.
if platform.system() != 'Darwin':
    raise NotImplementedError('Only Mac is supported at this time')

# Load Configuration
config_file = os.environ.get('CONFIG_FILE') or './config/custodial.yml'
with open(config_file, 'r') as ymlfile:
    config = yaml.load(ymlfile)


chrome_history.make_local_copy(config)
urls = chrome_history.get_urls(config)
