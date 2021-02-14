from configparser import ConfigParser

import controller
from wrappers import cmd
from .basemodule import BaseModule


class Library(BaseModule):

    # TODO: Four initial commands
    #   Get url for a book
    #   Add new book
    #   Remove a book
    #   List all books

    def __init__(self, _config: ConfigParser):
        self.config = _config

    def process(self, cont: 'controller.Controller', source: str, code: str, send_to: str, line: list):
        pass

    # -- Commands -- #

    @cmd()
    def lib(self, cont: 'controller.Controller', source: str, code: str, send_to: str, params: list):
        cont.chat(send_to, "Not yet implemented.")
