import importlib
import traceback
from configparser import ConfigParser

import controller
import modules


class Manager:

    def __init__(self, _config: ConfigParser):
        """
        Reloadable manager that parses and delegates commands to content modules.
        """
        self.config = _config
        self.module_dict = {}
        self.load_modules()

    # noinspection PyTypeChecker
    def load_modules(self):
        """
        Reloads all content modules, and fills main dictionary.
        """
        importlib.reload(modules)
        importlib.reload(modules.basemodule)
        importlib.reload(modules.general)
        importlib.reload(modules.kraken)
        importlib.reload(modules.lewd)
        importlib.reload(modules.library)
        importlib.reload(modules.rolls)

        self.module_dict = {
            "general": modules.general.General(self.config),
            "kraken": modules.kraken.Kraken(self.config),
            "lewd": modules.lewd.Lewd(self.config),
            "library": modules.library.Library(self.config),
            "rolls": modules.rolls.Rolls(self.config)
        }

    def parse(self, cont: 'controller.Controller', code: str, line: list[str]):
        """
        Parses additional information from an IRC message, then tries to send command to content modules.

        :param cont: handler for IRC connection
        :param code: numeric IRC code
        :param line: list form of full IRC message
        """
        if len(line) >= 3:
            source = line[0]
            send_to = line[2]
            if '#' not in send_to:
                send_to = line[0][1:]

            # noinspection PyBroadException
            try:
                for mod in self.module_dict:
                    m: modules.BaseModule = self.module_dict[mod]
                    m.read(cont, source, code, send_to, line)
            except Exception:
                cont.chat(send_to, "Error! Check your logs.")
                print(traceback.format_exc())
