import configparser

config = configparser.ConfigParser()
config.read('config.ini', 'utf-8')
DIR_PATH = config['DEFAULT']['doc_dir_path']
POSTDB_PATH = config['DEFAULT']['db_path']
CONFIG_PATH = 'config.ini'
