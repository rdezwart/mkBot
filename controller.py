import importlib
import socket
import ssl
import traceback
from configparser import ConfigParser

import manager
import util


class Controller:
    irc: ssl.SSLSocket
    socket: socket.socket

    def __init__(self, config: ConfigParser):
        print("Initializing controller...")
        self.config = config

        self.manager = manager.Manager()

    def connect(self):
        server: str = self.config["bot"]["server"]
        port: int = int(self.config["bot"]["port"])

        self.socket = socket.socket()
        self.socket.settimeout(30)
        context: ssl.SSLContext = ssl.create_default_context()

        self.irc = context.wrap_socket(self.socket, server_hostname=server)
        self.irc.connect((server, port))

    def log_in(self):
        bot_nick = self.config["bot"]["nick"]
        bot_pass = self.config["bot"]["pass"]

        self.push_msg("USER {0} {1} {2} {3}".format(bot_nick, bot_nick, "*", bot_nick))
        self.push_msg("NICK {0}".format(bot_nick))
        self.push_msg("PASS {0}".format(bot_pass))
        self.irc.settimeout(1)

    def join_channels(self):
        chan_parser = ConfigParser()
        chan_parser.read("data/channels.ini")
        chan_list = chan_parser.sections()

        for chan in chan_list:
            clean_chan = "#{0}".format(chan.strip("#"))
            self.push_msg("JOIN {0}".format(clean_chan))

    def start_listening(self):
        old_msg = ""

        while True:
            msg = "{0}{1}".format(old_msg, self.pull_msg())
            while "\r\n" in msg:
                line = msg[:msg.index("\r\n")]
                if line != "":
                    print(line)
                    self.process_msg(line)
                msg = msg[msg.index("\r\n") + 2:]
            old_msg = msg

    def push_msg(self, msg):
        if len(msg) > 1:

            if msg[-2:] != "\r\n":
                msg = "{0}\r\n".format(msg)

            if msg.count("\r\n") > 1:
                print("Error: Too many messages at once.")
            else:
                print(msg[:-2])
                self.irc.send(bytes(msg, "UTF-8"))
        else:
            print("Error: Invalid message.")

    def pull_msg(self):
        try:
            text = self.irc.recv(2040).decode("UTF-8")
        except socket.timeout:
            return ""

        return text

    def chat(self, channel, msg):
        self.push_msg("PRIVMSG {0} :{1}".format(channel, msg))

    def process_msg(self, msg):
        line = msg.split()
        code = line[1]

        if len(line) > 1:
            if line[0] == "PING":
                self.push_msg("PONG {0}".format(code))
            elif code == "396":
                self.join_channels()
            else:
                send_to = line[2]
                if '#' not in send_to:
                    send_to = line[0][1:]

                # check reload
                self.check_reload(code, line, send_to)
                try:
                    pass
                    # pass to manager
                except:
                    self.chat(send_to, "Error! Check your logs.")
                    print(traceback.format_exc())

    def check_reload(self, code, line, send_to):
        if len(line) > 3 and code == "PRIVMSG":

            if line[3].lower() == ":{0}reload".format(util.command_prefix):
                try:
                    importlib.reload(manager)
                    self.manager = manager.Manager()
                except:
                    self.chat(send_to, "Error! Check your logs.")
                    print(traceback.format_exc())

                self.chat(send_to, "Reloaded!")
