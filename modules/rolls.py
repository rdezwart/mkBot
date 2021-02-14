from configparser import ConfigParser
from random import randint

import controller
from wrappers import cmd
from .basemodule import BaseModule


class Rolls(BaseModule):

    def __init__(self, _config: ConfigParser):
        self.config = _config

    def process(self, cont: 'controller.Controller', source: str, code: str, send_to: str, line: list):
        pass

    # -- Commands -- #

    @cmd()
    def roll(self, cont: 'controller.Controller', source: str, code: str, send_to: str, params: list):
        clean = self.prep_roll(params)
        if clean.count("Error") > 0:
            cont.chat(send_to, clean)
        else:
            results = self.make_roll(clean)
            if results.count("Error") > 0:
                cont.chat(send_to, results)
            else:
                cont.chat(send_to, results[0])

    # -- Helpers -- #

    @staticmethod
    def prep_roll(msg):
        msg = "".join(msg)
        chunks = msg.split('+')

        if len(chunks) > 20:
            return "Error - Too many dice. ({0} / 20)".format(len(chunks))

        for i in range(len(chunks)):
            c = chunks[i]

            if c.find('d') == 0:
                c = "{0}{1}".format("1", c)
            if c == "":
                c = "1d20"
            if c.count('d') > 1:
                return "Error - Invalid dice. ({0})".format(c)

            chunks[i] = c

        msg = '+'.join(chunks)
        return msg

    @staticmethod
    def make_roll(msg):
        chunks = msg.split('+')
        total = 0
        dice = []
        d_string = ""

        for c in chunks:
            data = c.split('d')
            data = list(map(int, data))

            if len(data) == 1:
                dice.append("{0}".format(data[0]))
                total += data[0]
            else:
                d_temp = ""
                for i in range(0, data[0]):
                    ran = randint(1, data[1])
                    d_temp = "{0}{1}+".format(d_temp, ran)
                    total += ran
                dice.append(d_temp.rstrip('+'))

            d_string = ", ".join(dice)

        final = "Rolled [{0}] for {1}! ({2})".format(msg, total, d_string)
        if len(chunks) == 1 and chunks[0][0] == "1":
            final = final.split('(')[0]

        results = [final, msg, total, d_string]
        return results
