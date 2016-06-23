#!/usr/bin/env python
import socket

class Superlegends(object):

    def __init__(self):
        self.defaultPort = 5577

        # I've yet to discover why this is 48
        self.magicColorOffset = 48
        self.onmsg = [0x71, 0x23, 0x0f, 0xa3]
        self.offmsg = [0x71, 0x24, 0x0f, 0xa4]

    def connect(self, ip, port = None):
        self.ip = ip
        if port is None:
            self.port = 5577
        else:
            self.port = port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip, self.port))

    def setColor(self, red, green, blue):
        prefix = [0x31]
        padding = [0x00, 0xf0, 0x0f]
        checksum = [self._calcChecksum(red, green, blue)]
        self._send(prefix + [ red, green, blue ] + padding + checksum)

    def turnOn(self):
        self._send(self.onmsg)

    def turnOff(self):
        self._send(self.offmsg)

    def _calcChecksum(self, red, green, blue):
        return (red + green + blue + self.magicColorOffset) % 256

    def _send(self, msg):
        self.socket.send(bytes(msg))
