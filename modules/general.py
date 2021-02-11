import importlib
import traceback

import manager
from wrappers import cmd
from .basemodule import BaseModule


class General(BaseModule):

    def __init__(self):
        pass

    def process(self, controller, sender, code, send_to, line):
        pass

    @cmd()
    def test(self, controller, sender, code, send_to, line):
        controller.chat(send_to, "Delegation test!")

    @cmd()
    def reload(self, controller, source, code, send_to, line):
        # noinspection PyBroadException
        try:
            # noinspection PyTypeChecker
            importlib.reload(manager)
            controller.manager = manager.Manager()
        except Exception:
            controller.chat(send_to, "Error! Check your logs.")
            print(traceback.format_exc())

        controller.chat(send_to, "Reloaded!")
