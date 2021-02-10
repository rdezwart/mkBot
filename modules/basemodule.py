from abc import ABC, abstractmethod


class BaseModule(ABC):

    def read(self, controller, sender, code, send_to, line):
        pass

    def delegate(self, irc, code, line):
        pass
