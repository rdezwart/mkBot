from configparser import ConfigParser

import util

if __name__ == "__main__":
    config = ConfigParser()
    if util.check_config(config):
        print("Config file OK.")
        pass
