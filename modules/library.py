import traceback
from configparser import ConfigParser, DuplicateSectionError

import controller
from wrappers import cmd
from .basemodule import BaseModule


class Library(BaseModule):

    def __init__(self, _config: ConfigParser):
        self.config = _config

        self.library = ConfigParser(interpolation=None)
        self.library.read("data/library.ini")

    def process(self, cont: 'controller.Controller', source: str, code: str, send_to: str, line: list[str]):
        pass

    # -- Commands -- #

    @cmd()
    def lib(self, cont: 'controller.Controller', source: str, code: str, send_to: str, params: list[str]):

        if len(params) > 0:
            action = params[0].upper()

            if action == "LIST":
                cont.chat(send_to, sorted(self.library.sections()))

            elif action == "ADD":
                if len(params) > 2:
                    old_section = params[1].upper()
                    url = params[2]

                    if "://" not in old_section:
                        # noinspection PyBroadException
                        try:
                            self.library.add_section(old_section)
                            if self.library.has_section(old_section):  # if added correctly
                                self.library.set(old_section, "url", url)
                                cont.chat(send_to, "{0} was added.".format(old_section))
                            else:
                                cont.chat(send_to, "Something went wrong.")
                        except DuplicateSectionError:  # if already exists
                            cont.chat(send_to, "Book already exists. Use SET to edit existing entry.")
                        except Exception:
                            print(traceback.format_exc())
                            cont.chat(send_to, "ConfigParser error! Check your logs.")
                    else:
                        cont.chat(send_to, "Name can't be a URL.")
                else:
                    cont.chat(send_to, "Usage: .lib add NAME URL")

            elif action == "DEL":
                if len(params) > 1:
                    old_section = params[1].upper()

                    if self.library.remove_section(old_section):
                        cont.chat(send_to, "{0} was removed.".format(old_section))
                    else:
                        cont.chat(send_to, "No such book.")
                else:
                    cont.chat(send_to, "Usage: .lib del NAME")

            elif action == "GET":
                if len(params) > 1:
                    old_section = params[1].upper()

                    if self.library.has_section(old_section):
                        cont.chat(send_to,
                                  "{0} - {1}".format(old_section, self.library.get(old_section, "url", raw=True)))
                    else:
                        cont.chat(send_to, "No such book.")
                else:
                    cont.chat(send_to, "Usage: .lib get NAME")

            elif action == "SET":
                if len(params) > 3:
                    old_section = params[1].upper()
                    new_section = params[2].upper()
                    url = params[3]

                    if "://" not in old_section and "://" not in new_section:
                        if self.library.has_section(old_section):
                            if old_section != new_section:
                                self.library.remove_section(old_section)
                                self.library.add_section(new_section)

                            self.library.set(new_section, "url", url)
                            cont.chat(send_to, "{0} was edited.".format(old_section))
                        else:
                            cont.chat(send_to, "No such book. Use ADD to create a new entry.")
                    else:
                        cont.chat(send_to, "Name can't be a URL.")
                else:
                    cont.chat(send_to, "Usage: .lib set OLD_NAME NEW_NAME URL")

            else:
                cont.chat(send_to, "Invalid subcommand.")

        else:
            cont.chat(send_to, "Please specify a subcommand: list, add, del, get, set")

        # Save changes
        with open("data/library.ini", "w") as configfile:
            self.library.write(configfile)
