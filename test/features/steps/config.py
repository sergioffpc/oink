import configparser

config = configparser.ConfigParser()
config.read('../oink.ini')

config_env_name = config['environment']['name']
config_env = config[config_env_name]
