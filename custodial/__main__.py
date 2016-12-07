from configparser import ConfigParser
import platform
import yaml


config_file = "./config/custodial.yml"

if platform.system() != 'Darwin':
  raise NotImplementedError('Only Mac is supported at this time')
#TEST THIS

