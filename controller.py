import socket
import ssl
from configparser import ConfigParser

import manager


class Controller:
    irc: ssl.SSLSocket
    socket: socket.socket

    def __init__(self, config: ConfigParser):
        """
        Core engine of mkBot!

        :param config: parser containing config data
        """
        print("Initializing controller...")
        self.config = config

        self.manager = manager.Manager()

    def connect(self):
        """
        Pulls info from `data/config.ini` and connects to the specified IRC server.
        """
        server: str = self.config["bot"]["server"]
        port: int = int(self.config["bot"]["port"])

        self.socket = socket.socket()
        self.socket.settimeout(30)
        context: ssl.SSLContext = ssl.create_default_context()

        self.irc = context.wrap_socket(self.socket, server_hostname=server)
        self.irc.connect((server, port))

    def log_in(self):
        """
        Pulls info from `data/config.ini` and sends login information.
        """
        bot_nick = self.config["bot"]["nick"]
        bot_pass = self.config["bot"]["pass"]

        self.push_msg("USER {0} {1} {2} {3}".format(bot_nick, bot_nick, "*", bot_nick))
        self.push_msg("NICK {0}".format(bot_nick))
        self.push_msg("PASS {0}".format(bot_pass))
        self.irc.settimeout(1)

    def join_channels(self):
        """
        Pulls info from `data/channels.ini` and connects to the specified channels.
        """
        chan_parser = ConfigParser()
        chan_parser.read("data/channels.ini")
        chan_list = chan_parser.sections()

        for chan in chan_list:
            clean_chan = "#{0}".format(chan.strip("#"))
            self.push_msg("JOIN {0}".format(clean_chan))

    def start_listening(self):
        """
        Begins core loop for pulling and processing messages from IRC.

        NOTE: Only call once.
        """
        old_msg = ""

        while True:
            new_msg = "{0}{1}".format(old_msg, self.pull_msg())
            while "\r\n" in new_msg:
                cln_msg = new_msg[:new_msg.index("\r\n")]
                if cln_msg != "":
                    self.process_msg(cln_msg)
                new_msg = new_msg[new_msg.index("\r\n") + 2:]
            old_msg = new_msg

    def pull_msg(self) -> str:
        """
        Tries to receive a message from the current IRC server.

        :return: a message from IRC, if one exists
        """
        try:
            text = self.irc.recv(2040).decode("UTF-8")
            return text
        except socket.timeout:
            return ""

    def push_msg(self, msg: str):
        """
        Sends a message to the current IRC server.

        :param msg: message to send to IRC
        """
        if len(msg) > 1:

            if msg[-2:] != "\r\n":
                msg = "{0}\r\n".format(msg)

            if msg.count("\r\n") > 1:
                print("Error: Too many messages at once.")
            else:
                self.irc.send(bytes(msg, "UTF-8"))
                if msg.split()[0] != "PONG":
                    print(msg[:-2])
        else:
            print("Error: Invalid message.")

    def chat(self, send_to: str, msg: str):
        """
        Shortcut for sending a "PRIVMSG" to the current IRC server.

        :param send_to: destination channel
        :param msg: message to send to destination
        """
        self.push_msg("PRIVMSG {0} :{1}".format(send_to, msg))

    def process_msg(self, msg: str):
        """
        Breaks down an IRC message into workable chunks, then sends it to the Manager for processing.

        :param msg: message from IRC
        """
        line: list = msg.split()

        if len(line) > 1:
            code = line[1]

            if line[0] == "PING":
                self.push_msg("PONG {0}".format(code))
            else:
                print(msg)

            if code == "396":
                self.join_channels()

            self.manager.parse(self, code, line)
