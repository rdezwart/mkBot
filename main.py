from configparser import ConfigParser

import util
from controller import Controller

if __name__ == "__main__":
    config = ConfigParser()
    if util.check_config(config):
        print("Config file OK.")

        bot = Controller(config)
        bot.connect()
        bot.log_in()
        bot.start_listening()
