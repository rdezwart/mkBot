import urllib.parse
from configparser import ConfigParser
from random import randint

import requests
import rule34

import controller
from wrappers import cmd
from .basemodule import BaseModule


class Lewd(BaseModule):

    def __init__(self, _config: ConfigParser):
        self.config = _config

        self.headers = {"User-Agent": self.config.get("esix", "agent", raw=True)}
        self.name = self.config.get("esix", "name", raw=True)
        self.key = self.config.get("esix", "key", raw=True)
        self.url = self.config.get("esix", "url", raw=True)

        self.rule34 = rule34.Sync()

    def process(self, cont: 'controller.Controller', source: str, code: str, send_to: str, line: list[str]):
        pass

    # -- Commands -- #

    @cmd()
    def lewd(self, cont: 'controller.Controller', source: str, code: str, send_to: str, params: list[str]):

        spec = False

        if len(params) > 0:

            if params[0].lower() == "e6" or params[0].lower() == "34":
                joined = " ".join(params[1:])
                spec = True
            else:
                joined = " ".join(params[0:])

            if spec and len(params) == 1:
                cont.chat(send_to, "Please specify some more tags, or use an asterisk for a wildcard.")

            search = urllib.parse.quote_plus(joined)

            if params[0] == "e6":
                data = self.search_esix(search)
            elif params[0] == "34":
                data = self.search_rule(search)
            else:
                data = self.search_esix(search)
                if data[0] == 0:
                    data = self.search_rule(search)

                if data[0] == 0:
                    data[1] = "No images found on e621 or r34!"

            cont.chat(send_to, data[1])

        else:
            cont.chat(send_to, "Please specify some more tags, or use an asterisk for a wildcard.")

    # -- Helpers -- #

    def search_esix(self, search):
        ret = [0, "No posts found on e621!"]

        esix_url = self.url.format(search)
        esix_get = requests.get(esix_url, headers=self.headers, auth=(self.name, self.key))

        try:
            posts = esix_get.json()["posts"]
            ret[0] = len(posts)

            if ret[0] > 0:
                ret[1] = posts[randint(0, len(posts) - 1)]["file"]["url"]
        except ValueError:
            ret[1] = "Error connecting to e621."

        return ret

    def search_rule(self, search):
        ret = [0, "No posts found on rule34!"]

        # noinspection PyBroadException
        try:
            posts = self.rule34.getImages(search)
            ret[0] = len(posts)

            if ret[0] > 0:
                ret[1] = posts[randint(0, len(posts) - 1)].file_url
        except Exception:
            ret[1] = "Error connected to rule34."

        return ret
