from .basemodule import BaseModule


class General(BaseModule):

    def __init__(self):
        pass

    def checkReload(self, controller, code, line, send_to):
        controller.check_reload(code, line, send_to)
