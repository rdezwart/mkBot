import importlib

import modules


class Manager:
    """

    """

    general: modules.General
    kraken: modules.Kraken
    lewd: modules.Lewd
    library: modules.Library
    rolls: modules.Rolls

    def __init__(self):
        self.load_modules()

    def load_modules(self):
        importlib.reload(modules.general)
        importlib.reload(modules.kraken)
        importlib.reload(modules.lewd)
        importlib.reload(modules.library)
        importlib.reload(modules.rolls)

        self.general = modules.General()
        self.kraken = modules.Kraken()
        self.lewd = modules.Lewd()
        self.library = modules.Library()
        self.rolls = modules.Rolls()
