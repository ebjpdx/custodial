import os
import yaml
import sqlalchemy


config_file = os.environ.get('CONFIG_FILE') or './config/custodial.yml'
with open(config_file, 'r') as ymlfile:
    config = yaml.load(ymlfile)

engine = sqlalchemy.create_engine(config['application_data'])

conn = engine.connect()
