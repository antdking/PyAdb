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

from __future__ import print_function
import socket
import time


class Adb():
    def __init__(self, host='127.0.0.1', port=5037):
        self.host = host
        self.port = port
        self.connection = None
        self.adb_connect()

    def adb_connect(self):
        """
        create a socket to the device, connect to it, and check it
        """
        if self.connection is not None:
            self.connection.close()
            self.connection = None
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        self.connection = s
        command = "host:transport-any"
        self.adb_write(command)
        self.adb_read()
        time.sleep(1)

    def adb_write(self, command):
        # first the command needs it's length adding as a prefix
        # this is in hex form, and must be 4 digits long
        if self.connection is None:
            raise Exception("Error: No connection has been set up")
        len_command = str(hex(len(command)))[2:].upper()
        while len(len_command) < 4:
            len_command = "".join(["0", len_command])
        command = "".join([len_command, command])
        self.connection.send(command)

    def adb_read(self):
        read_data = self.connection.recv(4096)
        return read_data[4:]

    def adb_command(self, command, tries=3, pause=0.0):
        tried = 0
        while tried < tries:
            tried += 1
            try:
                self.adb_write(command)
                time.sleep(pause)
                return_data = self.adb_read()
                if return_data:
                    return return_data
            except socket.error:
                self.adb_connect()
        raise Exception("Can not detect your device")

    @staticmethod
    def adb_status(data):
        if data[:4] == "OKAY":
            return True
        return False


class AdbFunctions(Adb):
    def adb_devices(self):
        command = "host:devices"
        return self.adb_command(command)

    def adb_shell_command(self, command):
        command = "shell:{}".format(command)
        return self.adb_command(command, pause=0.2)


if __name__ == '__main__':
    adb = AdbFunctions()
    print(adb.adb_devices())
    print(adb.adb_shell_command("ls /"))
