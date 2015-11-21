# Endpoint uses:
# 01 - LED control from console (Main priority for documentation)
# 81 - Probably NFC data transmission to console (Nice to know, but less useful)


# All known commands for endpoint 01:
# Packets to this endpoint seem to always start with 0x55
# EP byte1 byte2 - description
# 01 0x04 0xd2 - Unknown, no changes to pads
# 01 0x06 0xc0 - Immediately switch pad(s) to a single value
# 01 0x08 0xc2 - Immediately change the colour of one or all pad(s), fade and flash available
# 01 0x09 0xc3 - set 1 or all pad(s) to a colour with variable flash rates
# 01 0x0a 0xb1 - Unknown, no changes to pads
# 01 0x0a 0xb3 - Unknown, no changes to pads
# 01 0x0a 0xd4 - Unknown, no changes to pads
# 01 0x0e 0xc8 - Immediately switch pad(s) to set of colours
# 01 0x0f 0xb0 - Startup?
# 01 0x14 0xc6 - Fade pad(s) to value(s)
# 01 0x17 0xc7 - Flash all 3 pads with individual colours and rates, either change to new or return to old based on pulse count




# All known commands for endpoint 81:
# Unconfirmed that these are actually commands.
# packets containing NFC data seem to begin with 0x56
# EP byte1 byte2
# 81 0x01 0x00
# 81 0x01 0x01
# 81 0x01 0x02
# 81 0x01 0x03
# 81 0x01 0x04
# 81 0x01 0x05
# 81 0x01 0x06
# 81 0x01 0x07
# 81 0x01 0x08
# 81 0x01 0x09
# 81 0x01 0x0a
# 81 0x01 0x0b
# 81 0x01 0x0c
# 81 0x01 0x0d
# 81 0x01 0x0e
# 81 0x01 0x0f
# 81 0x01 0x10
# 81 0x01 0x11
# 81 0x01 0x12
# 81 0x01 0x13
# 81 0x01 0x14
# 81 0x01 0x15
# 81 0x01 0x16
# 81 0x01 0x17
# 81 0x01 0x18
# 81 0x01 0x19
# 81 0x01 0x1a
# 81 0x01 0x1b
# 81 0x01 0x1c
# 81 0x01 0x1d
# 81 0x01 0x1e
# 81 0x01 0x1f
# 81 0x01 0x20
# 81 0x01 0x21
# 81 0x01 0x22
# 81 0x01 0x23
# 81 0x01 0x24
# 81 0x01 0x25
# 81 0x01 0x26
# 81 0x01 0x27
# 81 0x01 0x28
# 81 0x01 0x29
# 81 0x01 0x2a
# 81 0x01 0x2b
# 81 0x01 0x2c
# 81 0x01 0x2d
# 81 0x01 0x2e
# 81 0x01 0x2f
# 81 0x01 0x30
# 81 0x01 0x31
# 81 0x01 0x32
# 81 0x01 0x33
# 81 0x01 0x34
# 81 0x01 0x35
# 81 0x01 0x36
# 81 0x01 0x37
# 81 0x01 0x38
# 81 0x01 0x39
# 81 0x01 0x3a
# 81 0x01 0x3b
# 81 0x01 0x3c
# 81 0x01 0x3d
# 81 0x01 0x3e
# 81 0x01 0x3f
# 81 0x09 0x00
# 81 0x09 0x01
# 81 0x09 0x02
# 81 0x09 0x03
# 81 0x09 0x04
# 81 0x09 0x05
# 81 0x09 0x06
# 81 0x09 0x07
# 81 0x09 0x08
# 81 0x09 0x09
# 81 0x09 0x0a
# 81 0x09 0x0b
# 81 0x09 0x0c
# 81 0x09 0x0d
# 81 0x09 0x0e
# 81 0x09 0x0f
# 81 0x09 0x10
# 81 0x09 0x11
# 81 0x09 0x12
# 81 0x09 0x13
# 81 0x09 0x14
# 81 0x09 0x15
# 81 0x09 0x16
# 81 0x09 0x17
# 81 0x09 0x18
# 81 0x09 0x19
# 81 0x09 0x1a
# 81 0x09 0x1b
# 81 0x09 0x1c
# 81 0x09 0x1d
# 81 0x09 0x1e
# 81 0x09 0x1f
# 81 0x09 0x20
# 81 0x09 0x22
# 81 0x09 0x23
# 81 0x09 0x24
# 81 0x09 0x25
# 81 0x09 0x28
# 81 0x09 0x29
# 81 0x09 0x2a
# 81 0x09 0x2b
# 81 0x09 0x2c
# 81 0x09 0x2e
# 81 0x09 0x2f
# 81 0x09 0x30
# 81 0x09 0x31
# 81 0x09 0x32
# 81 0x09 0x35
# 81 0x09 0x36
# 81 0x09 0x37
# 81 0x09 0x38
# 81 0x09 0x39
# 81 0x09 0x3a
# 81 0x09 0x3b
# 81 0x09 0x3c
# 81 0x09 0x3d
# 81 0x09 0x3e
# 81 0x09 0x3f
# 81 0x0a 0x2d
# 81 0x0a 0x2f
# 81 0x0a 0x31
# 81 0x0b 0x01
# 81 0x0b 0x02
# 81 0x0b 0x03
# 81 0x12 0x00
# 81 0x12 0x01
# 81 0x12 0x02
# 81 0x12 0x03
# 81 0x12 0x04
# 81 0x12 0x05
# 81 0x12 0x06
# 81 0x12 0x0d
# 81 0x12 0x17
# 81 0x12 0x19
# 81 0x12 0x1c
# 81 0x12 0x1d
# 81 0x12 0x21
# 81 0x12 0x24
# 81 0x12 0x2c
# 81 0x12 0x2e
# 81 0x12 0x2f
# 81 0x12 0x30
# 81 0x12 0x3d
# 81 0x12 0x3e
# 81 0x12 0x3f
# 81 0x19 0x01