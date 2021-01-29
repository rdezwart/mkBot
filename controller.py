import socket
import ssl
from configparser import ConfigParser

from manager import Manager


class Controller:
    irc: ssl.SSLSocket
    socket: socket.socket

    def __init__(self):
        print("Initializing controller...")
        self.config = ConfigParser()
        self.config.read("data/config.ini")

        self.manager = Manager()

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

        self.send("USER {0} {1} {2} {3}".format(bot_nick, bot_nick, "*", bot_nick))
        self.send("NICK {0}".format(bot_nick))
        self.send("PASS {0}".format(bot_pass))
        self.irc.settimeout(1)

    def send(self, msg):
        if len(msg) > 1:

            if msg[-2:] != "\r\n":
                msg = "{0}\r\n".format(msg)

            if msg.count("\r\n") > 1:
                print("Error: Too many messages at once.")
            else:
                print(msg[-2:])
                self.irc.send(bytes(msg, "UTF-8"))
        else:
            print("Error: Invalid message.")

    def receive(self):
        text: str
        try:
            text = self.irc.recv(2040).decode("UTF-8")
        except socket.timeout:
            text = "TIMEOUT"

        return text
