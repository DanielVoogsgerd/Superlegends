#!/usr/bin/env python
import socket
from functools import reduce
from operator import add


def hex2dec(hex):
    return int(hex, 16)


class Superlegends(object):
    def __init__(self):
        self.defaultPort = 5577

        self.onmsg = [0x71, 0x23, 0x0f]
        self.offmsg = [0x71, 0x24, 0x0f]

        self.socket = None
        self.ip = None
        self.port = 5577

    def connect(self, ip, port=None):
        self.ip = ip
        if port is not None:
            self.port = port

        socket.setdefaulttimeout(0.5)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip, self.port))

    def disconnect(self):
        self.socket.close()

    def set_color(self, red, green, blue):
        prefix = [0x31]
        padding = [0x00, 0xf0, 0x0f]
        self._send(prefix + [red, green, blue] + padding)

    def warm(self, brightness):
        prefix = [0x31, 0x00, 0x00, 0x00]
        padding = [0x0f, 0x0f]
        msg = prefix + [brightness] + padding

        self._send(msg)

    def on(self):
        self._send(self.onmsg)

    def off(self):
        self._send(self.offmsg)

    def status(self):
        self._send([0x81, 0x8a, 0x8b])
        raw_status = self._receive()
        status = self._parse_status(raw_status)

        if status is False:
            return False

        return status

    def _send(self, msg):
        checksum = self._checksum(msg)
        self.socket.send(bytes(msg + [checksum]))

    def _receive(self):
        msg = ''
        while len(msg) < 28:
            data = self.socket.recv(14).hex()
            msg += data

        msg_bytes_hex = [msg[i:i + 2] for i in range(0, len(msg), 2)]
        msg_bytes = (list(map(hex2dec, msg_bytes_hex)))

        return msg_bytes

    def _parse_status(self, raw_status):
        status = ([raw_status[0:2], raw_status[2], raw_status[3:5], raw_status[5], raw_status[6:9], raw_status[9:10],
                   raw_status[10:12], raw_status[12:13], raw_status[13:14]])
        if self._validate_status(status) is False:
            return False

        return status

    @staticmethod
    def _checksum(msg):
        return reduce(add, msg) % 256

    @staticmethod
    def _validate_status(response):
        return response[0] == [0x81, 0x44] and response[2] == [0x61, 0x21] and response[6] == [0x04, 0x00]
