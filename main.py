import time
from configparser import ConfigParser

import util
from controller import Controller

if __name__ == "__main__":
    config = ConfigParser()
    if util.check_config(config):
        print("Config file OK.")
        time.sleep(1)

        bot = Controller(config)
        bot.connect()
        bot.log_in()
        bot.start_listening()
