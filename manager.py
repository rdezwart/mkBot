import importlib
import traceback

import modules
from controller import Controller


class Manager:

    def __init__(self):
        """
        Reloadable manager that parses and delegates commands to content modules.
        """
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
            "general": modules.general.General(),
            "kraken": modules.kraken.Kraken(),
            "lewd": modules.lewd.Lewd(),
            "library": modules.library.Library(),
            "rolls": modules.rolls.Rolls()
        }

    def parse(self, controller: Controller, code: str, line: list):
        """
        Parses additional information from an IRC message, then tries to send command to content modules.

        :param controller: handler for IRC connection
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
                    m.read(controller, source, code, send_to, line)
            except Exception:
                controller.chat(send_to, "Error! Check your logs.")
                print(traceback.format_exc())
