import importlib
import traceback

import manager
from controller import Controller
from wrappers import cmd
from .basemodule import BaseModule


class General(BaseModule):

    def __init__(self):
        pass

    def process(self, controller: Controller, source: str, code: str, send_to: str, line: list):
        pass

    @cmd()
    def test(self, controller: Controller, source: str, code: str, send_to: str, line: list):
        controller.chat(send_to, "Delegation test!")

    @cmd()
    def reload(self, controller: Controller, source: str, code: str, send_to: str, line: list):
        # noinspection PyBroadException
        try:
            # noinspection PyTypeChecker
            importlib.reload(manager)
            controller.manager = manager.Manager()
        except Exception:
            controller.chat(send_to, "Error! Check your logs.")
            print(traceback.format_exc())

        controller.chat(send_to, "Reloaded!")
