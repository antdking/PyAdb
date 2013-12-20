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

from adb_core import AdbCore
from time import time


class AdbFunctions(AdbCore):
    def devices(self):
        command = "host:devices"
        return_data = self.command(command)
        if return_data:
            return return_data

    def shell_command(self, command):
        command = "shell:{}".format(command)
        return_data = self.command(command, pause=0.2)
        if return_data:
            return return_data

    def logcat(self, branch="", timeout=0.0):
        command = "shell:exec logcat"
        if branch:
            command = " -b ".join([command, branch])
        # we don't use the predefined command function. create a new socket
        if not self.connect():
            yield False
            return
        self.write(command)
        # this needs sorting, perhaps thread it?
        # it isn't killed until a block is processed
        if timeout:
            timeout += time()
        try:
            while True:
                return_data = self.read(raw=True)
                if return_data:
                    yield return_data
                else:  # connection broken
                    self.close_connection()
                    break
                if timeout:
                    if time() > timeout:
                        self.close_connection()
                        return
        except KeyboardInterrupt:
            return

    def interactive_shell(self):
        from adb_shell import AdbShell
        command = "shell:"
        if not self.connect():
            return
        self.write(command)
        self.read()
        adb_shell = AdbShell(self.connection)
        adb_shell.interact()