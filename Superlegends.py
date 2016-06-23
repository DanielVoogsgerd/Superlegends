#!/usr/bin/env python
import socket

class Superlegends(object):

    def __init__(self):
        self.defaultPort = 5577

        # I've yet to discover why this is 48 and 79
        self.magicColorOffset = 48
        self.magicWarmOffset = 79
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
        checksum = [self._calcColorChecksum(red, green, blue)]

        self._send(prefix + [ red, green, blue ] + padding + checksum)

    def warm(self, brightness):
        prefix = [0x31, 0x00, 0x00, 0x00]
        padding = [0x0f, 0x0f]
        msg = prefix + [brightness] + padding + [self._calcWarmChecksum(brightness)]

        self._send(msg)

    def on(self):
        self._send(self.onmsg)

    def off(self):
        self._send(self.offmsg)

    def _calcWarmChecksum(self, brightness):
        return (brightness + self.magicWarmOffset) % 256

    def _calcColorChecksum(self, red, green, blue):
        return (red + green + blue + self.magicColorOffset) % 256

    def _send(self, msg):
        self.socket.send(bytes(msg))
