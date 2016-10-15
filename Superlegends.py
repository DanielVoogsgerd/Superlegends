#!/usr/bin/env python
import socket
from functools import reduce
from operator import add

class Superlegends(object):

    def __init__(self):
        self.defaultPort = 5577

        self.onmsg = [0x71, 0x23, 0x0f]
        self.offmsg = [0x71, 0x24, 0x0f]

    def connect(self, ip, port = None):
        self.ip = ip
        if port is None:
            self.port = 5577
        else:
            self.port = port

        socket.setdefaulttimeout(0.5)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip, self.port))

    def disconnect(self):
        self.socket.close()

    def setColor(self, red, green, blue):
        prefix = [0x31]
        padding = [0x00, 0xf0, 0x0f]
        self._send(prefix + [ red, green, blue ] + padding)

    def warm(self, brightness):
        prefix = [0x31, 0x00, 0x00, 0x00]
        padding = [0x0f, 0x0f]
        msg = prefix + [brightness] + padding

        self._send(msg)

    def on(self):
        self._send(self.onmsg)

    def off(self):
        self._send(self.offmsg)

    def _send(self, msg):
        checksum = reduce(add, msg) % 256
        self.socket.send(bytes(msg + [checksum]))
