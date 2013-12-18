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
from adb_core import AdbCore


class AdbFunctions(AdbCore):
    def adb_devices(self):
        command = "host:devices"
        return self.adb_command(command)

    def adb_shell_command(self, command):
        command = "shell:{}".format(command)
        return self.adb_command(command, pause=0.5)

    def adb_logcat(self, branch=""):
        command = "shell:exec logcat"
        if branch:
            command = " -b ".join([command, branch])
        # we don't use the predefined command function. create a new socket
        self.adb_connect()
        self.adb_write(command)
        # this needs sorting, perhaps thread it?
        # it isn't killed until a block is processed
        try:
            while True:
                yield self.connection.recv(4096)
        except KeyboardInterrupt:
            pass
