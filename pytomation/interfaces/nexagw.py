"""
File:
    nexagw.py

Erik Traedal <erik.traedal@gmail.com>
Copyright (c), 2014

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
MA 02110-1301, USA.



Author(s):
    Erik Traedal <erik.traedal@gmail.com>
    Copyright (c), 2014


License:
    This free software is licensed under the terms of the GNU public license,
    Version 3

Usage:
    To be used for sending messages to Nexa/HomeEasy etc. devices using an Arduino and some very cheap hardware.
    The Arduino code and instructions are located here: https://github.com/ErikLove/NexaGw
    There are two parameters, the first being the remote code as a binary string, the second being the device id as a string ('00', '01' or '10')

Example:
    nexagw = NexaGw(Serial('/dev/ttyUSB0',9600))
    l_window = Light(address=('00111010000010110011011110','01'),devices=(nexagw, loc_home), name="Christmas star in window")


Versions and changes:
    Initial version created on Dec 29, 2014
    2014/12/29 - 1.0 - Initial version

"""
import threading
import time
import re
from Queue import Queue
from binascii import unhexlify

from .common import *
from .ha_interface import HAInterface

class NexaGw(HAInterface):
    VERSION = '1.0'
    MODEM_PREFIX = ''

    def __init__(self, interface, *args, **kwargs):
        super(NexaGw, self).__init__(interface, *args, **kwargs)

    def _init(self, *args, **kwargs):
        super(NexaGw, self)._init(*args, **kwargs)

        self.version()
        self.ready = True   # if interface is ready to rx command

    def _readInterface(self, lasPacketHash):
        time.sleep(0.5)


    def _sendInterfaceCommand(self, remote, device, state):
        command = 'S' + remote + '0' + state + '00' + device + 'P'
        self._interface.write(command)
        self._logger.info("[NexaGw] Sending command>" + command)

    def on(self, address):
        remote = address[0]
        device = address[1]
        self._logger.info("[NexaGw] Sending ON to device> " + device)
        self._sendInterfaceCommand(remote, device, '1')

    def off(self, address):
        remote = address[0]
        device = address[1]
        self._logger.info("[NexaGw] Sending OFF to device> " + device)
        self._sendInterfaceCommand(remote, device, '0')

    def version(self):
        self._logger.info("NexaGw Pytomation driver version " + self.VERSION + '\n')

