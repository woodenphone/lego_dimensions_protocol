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
import threading

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



def generate_checksum_for_command(command):
    """
    Given a command (without checksum or trailing zeroes),
    generate a checksum for it.
    """
    assert(len(command) <= 31)
    # Add bytes, overflowing at 256
    result = 0
    for word in command:
        result = result + word
        if result >= 256:
            result -= 256
    return result


def pad_message(message):
    """Pad a message to 32 bytes"""
    assert(len(message) <= 32)
    while(len(message) < 32):
        message.append(0x00)
    return message


def convert_command_to_packet(command):
    assert(len(command) <= 31)
    checksum = generate_checksum_for_command(command)
    message = command+[checksum]
    packet = pad_message(message)
    return packet


def send_command(command, silent=False):
    packet = convert_command_to_packet(command)
    if not silent:
        print("packet:"+repr(packet))
    dev.write(1, packet)


def follow_tag():
    """
    Light up the pad that most recently had a tag placed on it
    """
    red, green, blue = (0xff,0x00,0xff)
    while True:
        try:
            inwards_packet = dev.read(0x81,32, timeout=100)
            print("inwards_packet:"+repr(inwards_packet))
            bytelist = list(inwards_packet)
            print("bytelist:"+hex_repr(bytelist))

            if not bytelist:# We need a packet
                continue
            if bytelist[0] != 0x56:# Only listen to NFC packets
                continue

            pad_num = bytelist[2]
            tag_id = bytelist[6:12]
            removed = bool(bytelist[5])# Was the tag removed, if false it was added

            if not removed:
                # Blank pads
                send_command(
                    [0x55, 0x06, 0xc0, 0x02, 0, 0, 0, 0,],
                    silent=False
                    )
                # Set pad to colour
                send_command(
                    [0x55, 0x06, 0xc0, 0x02, pad_num, red, green, blue,],
                    silent=False
                    )
        except usb.USBError, err:
            pass






def watch_returned():
    """Send a command on endpoint 01 and watch endpoint 81 to see if anything happens"""
    commands = [

        ]
    for command in commands:
        print("command: "+hex_repr(command))
        dev.write(1, command)
        time.sleep(2)

def main():
    init_usb()
    follow_tag()
    return

if __name__ == '__main__':
    main()
