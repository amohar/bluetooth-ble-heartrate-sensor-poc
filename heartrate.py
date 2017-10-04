#!/usr/bin/python
"""
heartrate.py

This is a POC application to see if and how I could communicate with a speciffic
Bluetooth BLE device. The device of choice is Suunto heartrate sensor.
"""

import struct
from bluepy.btle import Scanner, DefaultDelegate, Peripheral, BTLEException

HCI_IDX = 0

class ScanDelegate(DefaultDelegate):
    """
    This class implements a method which handles the detection of the newly
    discovered Suunto devices.
    """
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        """
        If a newly discovered device is the expected one, we subscribe a callback to handle the
        notifications. We also get the desired characteristic and start the notification process.
        """
        if isNewDev and (9 in dev.scanData.keys()) and dev.scanData[9] == "Suunto Smart Sensor":
            per = Peripheral(dev.addr).withDelegate(NotificationDelegate(dev.addr))

            svc = per.getServiceByUUID("0000180d-0000-1000-8000-00805f9b34fb")
            char = svc.getCharacteristics("00002a37-0000-1000-8000-00805f9b34fb")[0]

            ch_handle = char.getHandle()
            per.writeCharacteristic(ch_handle + 1, struct.pack("<bb", 0x01, 0x00))

            while True:
                if per.waitForNotifications(1.0):
                    continue

class NotificationDelegate(DefaultDelegate):
    """
    his class implements a method which handles the notifications received from a
    device. We are expecting only the messages of size four. We split them in four
    integers (values up to 255). The heartrate is the second one, we discard the rest.
    """

    _addr = ""

    def __init__(self, addr):
        DefaultDelegate.__init__(self)

        self._addr = addr

    def handleNotification(self, cHandle, data):
        if len(data) == 4:
            (_, heartrate, _, _) = struct.unpack("cccc", data)
            print self._addr + ":  \033[31m" + u"\u2764 " + str(ord(heartrate)) + "\033[0m"

    def _unpack(self, data):
        res = ""
        for char in data:
            res += str(ord(char)) + " "

        return res

def scan():
    """
    Starts the scanning process on the desired Bluetooth device.
    """
    scanner = Scanner(HCI_IDX).withDelegate(ScanDelegate())
    try:
        scanner.scan(0)
    except BTLEException as ex:
        print "Exception happened. " + ex.message

def main():
    """
    Starts the whole program. Can be used to parse arguments if needed in the future.
    """
    scan()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "\nExiting."
