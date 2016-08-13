from configparser import ConfigParser

from .paths import ARCRANK_DATA_PATH


CONFIG_FILE = ARCRANK_DATA_PATH / "config.ini"

config = ConfigParser()
config.read(CONFIG_FILE)
