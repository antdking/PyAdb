"""
Copyright (C) 2013 Cybojenix <anthonydking@slimroms.net>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from socket import socket, AF_INET, SOCK_STREAM, SHUT_RDWR
from time import sleep


class AdbCore():
    def __init__(self, host='127.0.0.1', port=5037):
        self.host = host
        self.port = port
        self.connection = None
        self.connect()

    def connect(self):
        """
        create a socket to the device, connect to it, and check it
        """
        if self.connection is not None:
            self.close_connection()
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((self.host, self.port))
        self.connection = s
        command = "host:transport-usb"
        self.write(command)
        read_data = self.read(raw=True)
        if self.status(read_data):
            return 1

    def close_connection(self):
        self.connection.shutdown(SHUT_RDWR)
        self.connection.close()
        self.connection = None

    def write(self, command):
        # first the command needs it's length adding as a prefix
        # this is in hex form, and must be 4 digits long
        len_command = str(hex(len(command)))[2:].upper()
        while len(len_command) < 4:
            len_command = "".join(["0", len_command])
        command = "".join([len_command, command])
        self.connection.send(command)

    def read(self, raw=False, buff=4096):
        read_data = self.connection.recv(buff)
        if not raw:
            read_data = read_data[4:]
        return read_data

    def read_stream(self, raw=False, buff=4096):
        pass

    def command(self, command, pause=0.0):
        # a new socket must be created for every command
        if not self.connect():
            return 0
        self.write(command)
        sleep(pause)
        return_data = self.read(raw=True)
        if self.status(return_data):
            return return_data[4:]
        return 0

    @staticmethod
    def status(data):
        if data[:4] == "OKAY":
            return True
        return False

if __name__ == '__main__':
    adb = AdbCore()
    adb.connect()