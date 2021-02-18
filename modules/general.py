import importlib
import traceback
from configparser import ConfigParser

import controller
import manager
from wrappers import cmd
from .basemodule import BaseModule


class General(BaseModule):

    def __init__(self, _config: ConfigParser):
        self.config = _config

    def process(self, cont: 'controller.Controller', source: str, code: str, send_to: str, line: list[str]):
        pass

    # -- Commands -- #

    @cmd()
    def test(self, cont: 'controller.Controller', source: str, code: str, send_to: str, params: list[str]):
        cont.chat(send_to, "Delegation test!")

    @cmd()
    def raw(self, cont: 'controller.Controller', source: str, code: str, send_to: str, params: list[str]):
        if len(params) > 0:
            cont.push_msg(" ".join(params))

    @cmd()
    def reload(self, cont: 'controller.Controller', source: str, code: str, send_to: str, params: list[str]):
        # noinspection PyBroadException
        try:
            cont.manager.module_dict["lewd"].rule34.sessionClose()

            # noinspection PyTypeChecker
            importlib.reload(manager)
            cont.manager = manager.Manager(cont.config)

        except Exception:
            cont.chat(send_to, "Error! Check your logs.")
            print(traceback.format_exc())

        cont.chat(send_to, "Reloaded!")
