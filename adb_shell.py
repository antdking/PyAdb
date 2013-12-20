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

import socket
from threading import Thread, Event
from sys import stdout


def _read_adb(sock, writer):
        try:
            return_data = sock.recv(4096)
            if return_data:
                writer(return_data)
            else:
                pass
        except socket.timeout:
            pass
        except socket.error:
            return 1


class AdbThread(Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        self.kill_event = Event()
        Thread.__init__(self)

    def run(self):
        while not self.kill_event.is_set():
            if self._target(*self._args):
                self.kill_event.set()


class AdbShell:
    def __init__(self, sock):
        self.sock = sock
        sock.settimeout(0.5)
        self.read_thread = None

    def interact(self):
        banner = "Welcome to PyAdb Interactive Shell"
        self.write("%s\n" % banner)
        self.write(self.read())
        self.read_thread = AdbThread(_read_adb, self.sock, self.write)
        self.read_thread.start()
        while True:
            if self.read_thread.kill_event.is_set():
                return self.kill()
            try:
                try:
                    line = raw_input()
                    if self.push(line):
                        return 1
                except EOFError:  # in our case, it's always ctrl c, z, or d
                    return self.kill()
            except KeyboardInterrupt:
                return self.kill()

    @staticmethod
    def write(data):
        stdout.write(data)

    def read(self):
        return self.sock.recv(4096)

    def push(self, line):
        try:
            self.sock.sendall(line)
            self.sock.sendall("\r")
        except socket.error:
            return self.kill()

    def kill(self):
        self.read_thread.kill_event.set()
        self.read_thread.join()
        return 1
