from abc import ABC, abstractmethod

import util


class BaseModule(ABC):

    def read(self, controller, sender, code, send_to, line):
        self.process(controller, sender, code, send_to, line)
        self.delegate(controller, sender, code, send_to, line)

    @abstractmethod
    def process(self, controller, sender, code, send_to, line):
        pass

    def delegate(self, controller, sender, code, send_to, line):
        if len(line) >= 4 and len(line[3]) > 1:
            if line[3][1] == util.command_prefix:
                cmd_name = line[3][2:].lower()
                cmd_func = getattr(self, cmd_name, None)

                if callable(cmd_func) and hasattr(cmd_func, "is_command"):
                    cmd_func(controller, sender, code, send_to, line)
