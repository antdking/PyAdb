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
from adb_functions import AdbFunctions

if __name__ == '__main__':
    adb = AdbFunctions()

    # adb devices demonstration
    adb_devices = adb.devices()
    if adb_devices:
        print(adb_devices)
    else:
        print("adb device: device can not be found")

    # adb shell commands
    shell_command = adb.shell_command("su -c 'ls /dev/log'")
    if shell_command:
        print(shell_command)
    else:
        print("shell command: device can not be found")

    # adb raw commands
    adb_command = adb.command("host:version")
    if adb_command:
        print(adb_command)
    else:
        print("raw commands: device can not be found")

    # adb logcat
    for log_block in adb.logcat(timeout=5):
        if log_block:
            print(log_block)
        else:
            print("logcat: device disconnected")

    print("loading interactive shell")
    adb.interactive_shell()