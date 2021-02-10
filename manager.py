import importlib
import traceback

import modules


class Manager:

    def __init__(self):
        self.module_dict = {}
        print("Manager")
        self.load_modules()

    # noinspection PyTypeChecker
    def load_modules(self):
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

    def parse(self, controller, code, line):
        if len(line) >= 3:

            source = line[0]
            send_to = line[2]
            if '#' not in send_to:
                send_to = line[0][1:]

            self.module_dict["general"].checkReload(controller, code, line, send_to)

            # noinspection PyBroadException
            try:
                for mod in self.module_dict:
                    m: modules.BaseModule = self.module_dict[mod]
                    m.read(controller, source, code, send_to, line)
            except Exception:
                controller.chat(send_to, "Error! Check your logs.")
                print(traceback.format_exc())
