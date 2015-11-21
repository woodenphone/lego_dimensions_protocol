#-------------------------------------------------------------------------------
# Name:        library
# Purpose:     Python library to control Lego Dimensions gateway/portal peripheral
#              Xbox version is unsupported due to likely harware differences.
# Author:      User
#
# Created:     21/11/2015
# Copyright:   (c) User 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------


# Command to function mapping:
# EP Cmd1 Cmd2 - func_name() - Description
# 01 0x06 0xc0 - switch_pad() - Immediately switch pad(s) to a single value
# 01 0x08 0xc2 - Immediately change the colour of one or all pad(s), fade and flash available
# 01 0x09 0xc3 - flash_pad() -set 1 or all pad(s) to a colour with variable flash rates
# 01 0x0e 0xc8 - Immediately switch pad(s) to set of colours
# 01 0x14 0xc6 - Fade pad(s) to value(s)
# 01 0x17 0xc7 - Flash all 3 pads with individual colours and rates, either change to new or return to old based on pulse count




class Gateway():
    """
    Represents a Lego Dimensions gateway/portal peripheral
    """
    def __init__(self):
        # Initialise USB connection to the device
        self.dev = self._init_usb()
        return

    def _init_usb(self):
        """
        Connect to and initialise the portal
        """
        import usb.core
        import usb.util
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

    def generate_checksum_for_command(self,command):
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

    def pad_message(self,message):
        """Pad a message to 32 bytes"""
        assert(len(message) <= 32)
        while(len(message) < 32):
            message.append(0x00)
        return message

    def convert_command_to_packet(self,command):
        """Take a command and add a checksum and padding"""
        assert(len(command) <= 31)
        checksum = self.generate_checksum_for_command(command)
        message = command+[checksum]
        packet = self.pad_message(message)
        return packet

    def send_command(self,command):
        """Take the command, add checksum and padding, then send it"""
        packet = self.convert_command_to_packet(command)
        print("packet:"+repr(packet))
        self.dev.write(1, packet)

    def switch_pad(self,pad,red,green,blue):
        """
        Change the colour of one or all pad(s) immediately
        Pad numbering: 0:All, 1:Center, 2:Left, 3:Right
        Colour values are 0-255, with 0 being off and 255 being maximum
        Abstraction for command: 0x06 0xc0
        """
        command = [0x55, 0x06, 0xc0, 0x02, pad, red, green, blue,]
        self.send_command(command)
        return

    def flash_pad(self, pad, on_length, off_length, pulse_count, red, green, blue):
        """
        Flash one or all pad(s) a given colour
        The pad(s) will either revert to old colour or stay on the new one depending on the pulse_count value
        Odd: keep new colour, Even: keep previous colour. Exception: 0x00 keeps new colour.
        Pulse counts from 0xff will flash forever.
        Pad numbering: 0:All, 1:Center, 2:Left, 3:Right
        Colour values are 0-255, with 0 being off and 255 being maximum
        Abstraction for command: 0x09 0xc3
        """
        command = [0x55, 0x09, 0xc3, 0x1f, pad, on_length, off_length, pulse_count, red, green, blue]
        self.send_command(command)
        return

    def fade_pad(self, pad, speed, pulse_count, red, green, blue):# TODO
        """
        ... one or all pad(s) a given colour
        The pad(s) will either revert to old colour or stay on the new one depending on the pulse_count value TODO CHECK THIS IS TRUE
        Odd: keep new colour, Even: keep previous colour. Exception: 0x00 keeps new colour. TODO CHECK THIS IS TRUE
        Pulse counts from 0xff will flash forever. TODO CHECK THIS IS TRUE
        Pad numbering: 0:All, 1:Center, 2:Left, 3:Right
        Colour values are 0-255, with 0 being off and 255 being maximum
        Abstraction for command: 0x08 0xc2
        """
        command = []
        self.send_command(command)
        return


def debug():
    """For testing and debugging and coding and stuff"""
    import time
    # Get gateway object
    gateway = Gateway()
    # Test switch_pad()
    gateway.switch_pad(
        pad=0,
        red=255,
        green=255,
        blue=0,
        )
    time.sleep(5)
    # Test flash_pad()
    gateway.flash_pad(
        pad = 0,
        on_length = 10,
        off_length = 20,
        pulse_count = 100,
        red = 0,
        green = 0,
        blue = 0
        )
    # Test fade_pads(


def main():
    debug()
    pass

if __name__ == '__main__':
    main()
