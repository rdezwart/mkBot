from abc import ABC, abstractmethod

import controller
import util


class BaseModule(ABC):

    def read(self, cont: 'controller.Controller', source: str, code: str, send_to: str, line: list):
        """
        Base method for preparing commands.

        :param cont: handler for IRC connection
        :param source: source of IRC message
        :param code: numeric IRC code
        :param send_to: return location of IRC message
        :param line: list form of full IRC message
        """
        self.process(cont, source, code, send_to, line)
        self.delegate(cont, source, code, send_to, line)

    @abstractmethod
    def process(self, cont: 'controller.Controller', source: str, code: str, send_to: str, line: list):
        """
        Abstract method for any additional processing before delegation.

        :param cont: handler for IRC connection
        :param source: source of IRC message
        :param code: numeric IRC code
        :param send_to: return location of IRC message
        :param line: list form of full IRC message
        """
        pass

    def delegate(self, cont: 'controller.Controller', source: str, code: str, send_to: str, line: list):
        """
        If a registered command (parsed from IRC message) exists in current content module, call it.

        :param cont: handler for IRC connection
        :param source: source of IRC message
        :param code: numeric IRC code
        :param send_to: return location of IRC message
        :param line: list form of full IRC message
        """
        if len(line) >= 4 and len(line[3]) > 1:
            if line[3][1] == util.command_prefix:
                cmd_name = line[3][2:].lower()
                cmd_func = getattr(self, cmd_name, None)
                params = line[4:]

                if callable(cmd_func) and hasattr(cmd_func, "is_command"):
                    cmd_func(cont, source, code, send_to, params)
