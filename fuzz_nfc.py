#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      User
#
# Created:     22/11/2015
# Copyright:   (c) User 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import usb
import usb.core
import usb.util
import time

def init_usb():
    global dev
    # find our device
    dev = usb.core.find(idVendor=0x0e6f)# 0x0e6f Logic3 (made lego dimensions portal hardware)

    # was it found?
    if dev is None:
        raise ValueError('Device not found')

    # set the active configuration. With no arguments, the first
    # configuration will be the active one
    dev.set_configuration()

    # Initialise portal
    print "Initialising portal"
    dev.write(1, [0x55, 0x0f, 0xb0, 0x01, 0x28, 0x63, 0x29, 0x20, 0x4c, 0x45, 0x47, 0x4f, 0x20, 0x32, 0x30, 0x31, 0x34, 0xf7, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])# Startup
    return dev


def hex_repr(bytelist):
    output = ""
    for value in bytelist:
        output += str(hex(value))+", "
    return output[:-2]


def watch_pads():
    while True:
        try:
            inwards_packet = dev.read(0x81,32, timeout=100)
            bytelist = list(inwards_packet)
            print("inwards_packet:"+hex_repr(bytelist))
        except usb.USBError, err:
            pass


def main():
    init_usb()
    watch_pads()
    return

if __name__ == '__main__':
    main()
