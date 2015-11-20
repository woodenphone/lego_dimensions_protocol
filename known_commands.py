#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      User
#
# Created:     16/11/2015
# Copyright:   (c) User 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import usb.core
import usb.util
import time

# find our device
dev = usb.core.find(idVendor=0x0e6f)# 0x0e6f Logic3 (made lego dimensions portal hardware)

# was it found?
if dev is None:
    raise ValueError('Device not found')

# set the active configuration. With no arguments, the first
# configuration will be the active one
dev.set_configuration()

# Initialise portal
print dev.write(1, [0x55, 0x0f, 0xb0, 0x01, 0x28, 0x63, 0x29, 0x20, 0x4c, 0x45, 0x47, 0x4f, 0x20, 0x32, 0x30, 0x31, 0x34, 0xf7, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])# Startup



# Pad color notation used in comments:
# Left, center, right
# l:colour, c: colour:, r: colour




# General command structure for endpoint 01
# 0x55 Magic number
# command byte 1
# command byte 2
# message counter, no noticed effect
# args...
# checksum, (simple addition of previous bytes with overflow at 255)
# padding to 32 bytes


# Noticed argument conventions
# Pad numbering:
# 0x01, 0x02, 0x03
# Colour ordering
# Red, green, blue
# Colour values 1 byte in length
# 0x00: off, 0xff: maximum brightness


# Checksum characteristics
# 1 Byte in size
# Always the last non-zero byte (Unknown what happens if checksum turns out to be zero)
# Reordering message bytes does not invalidate checksum
# Message counter affects checksum
# Simple addition of previous bytes with overflow at 255




# Commands 0x01 0xXX - all tried have no visible effect, short/no arguments




# 0x04 0x02
# Unknown effect, does not turn on pads?
# Byte: use
# 0: Always 0x55
# 1: 0x04 cmd
# 2: 0x02 cmd
# 3: Message counter
# 4: ?
# 5: ?
# 6: Checksum?
# 7-31: Padding




# 0x0a 0xb3
# Unknown effect, does not turn on or off pads
# Byte: use
# 0: Always 0x55
# 1: 0x0a cmd
# 2: 0xb3 cmd
# 3: Message counter
# 4:
# 5:
# 6:
# 7:
# 8:
# 9:
# 10:
# 11:
# 12: Checksum
# 13-31: Padding




# 0x04 0xd2
# Unknown effect, does not turn on or off pads
# Byte: use
#0: Always 0x55
#1: 0x04 cmd
#2: 0xd2 cmd
#3: Message counter
#4: ?
#5: ?
#6: Checksum?
#7-31: Padding








def main():
    pass

if __name__ == '__main__':
    main()
