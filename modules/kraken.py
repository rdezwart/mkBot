from configparser import ConfigParser

import controller
from wrappers import cmd
from .basemodule import BaseModule


class Kraken(BaseModule):

    def __init__(self, _config: ConfigParser):
        self.config = _config

    def process(self, cont: 'controller.Controller', source: str, code: str, send_to: str, line: list):
        pass

    # -- Commands -- #

    @cmd()
    def kraken(self, cont: 'controller.Controller', source: str, code: str, send_to: str, params: list):
        cont.chat(send_to, "Not yet implemented.")
