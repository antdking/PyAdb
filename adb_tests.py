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
    print(adb.adb_devices())

    # adb shell commands
    print(adb.adb_shell_command("su -c 'ls /dev/log/'"))

    # adb raw commands
    print(adb.adb_command("host:version"))

    # adb logcat
    for log_block in adb.adb_logcat(branch="radio"):
        print(log_block)