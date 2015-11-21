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
# 01 0x06 0xc0 - switch_pad() - Immediately switch one or all pad(s) to a single value
# 01 0x08 0xc2 - fade_pad() - Immediately change the colour of one or all pad(s), fade and flash available
# 01 0x09 0xc3 - flash_pad() - set 1 or all pad(s) to a colour with variable flash rates
# 01 0x0e 0xc8 - switch_pads() - Immediately switch pad(s) to set of colours
# 01 0x14 0xc6 - TODO - Fade pad(s) to value(s)
# 01 0x17 0xc7 - TODO - Flash all 3 pads with individual colours and rates, either change to new or return to old based on pulse count


import time

class Gateway():
    """
    Represents a Lego Dimensions gateway/portal peripheral
    """
    def __init__(self,verbose=True):
        self.verbose = verbose
        # Initialise USB connection to the device
        self.dev = self._init_usb()
        # Reset the state of the device to all pads off
        self.blank_pads()
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
        if self.verbose:
            print "Initialising portal"
        dev.write(1, [0x55, 0x0f, 0xb0, 0x01, 0x28, 0x63, 0x29, 0x20, 0x4c, 0x45, 0x47, 0x4f, 0x20, 0x32, 0x30, 0x31, 0x34, 0xf7, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])# Startup
        return dev

    def generate_checksum_for_command(self,command):
        """
        Given a command (without checksum or trailing zeroes),
        generate a checksum for it.
        """
        assert(len(command) <= 31)# One byte must be left for the checksum
        # Add bytes, overflowing at 256
        result = 0
        for word in command:
            result = result + word
            if result >= 256:
                result -= 256
        return result

    def pad_message(self,message):
        """Pad a message to 32 bytes"""
        assert(len(message) <= 32)# Messages cannot be longer than 32 bytes
        while(len(message) < 32):
            message.append(0x00)
        return message

    def convert_command_to_packet(self,command):
        """Take a command and add a checksum and padding"""
        assert(len(command) <= 31)# One byte must be left for the checksum
        checksum = self.generate_checksum_for_command(command)
        message = command+[checksum]
        packet = self.pad_message(message)
        return packet

    def send_command(self,command):
        """Take the command, add checksum and padding, then send it"""
        assert(len(command) <= 31)# One byte must be left for the checksum
        packet = self.convert_command_to_packet(command)
        if self.verbose:
            print("packet:"+repr(packet))
        self.dev.write(1, packet)

    def blank_pads(self):
        """
        Clear the pads to all off.
        """
        self.switch_pad(
            pad = 0, # All pads
            colour=(0,0,0)# RGB
            )
        return

    def switch_pad(self, pad, colour):
        """
        Change the colour of one or all pad(s) immediately
        Pad numbering: 0:All, 1:Center, 2:Left, 3:Right
        Colour values are 0-255, with 0 being off and 255 being maximum
        Colour should be a tuple of 0-255 values in the format (red, green,blue)
        Abstraction for command: 0x06 0xc0
        """
        red, green, blue = colour[0], colour[1], colour[2]
        command = [0x55, 0x06, 0xc0, 0x02, pad, red, green, blue,]
        self.send_command(command)
        return

    def flash_pad(self, pad, on_length, off_length, pulse_count, colour):
        """
        Flash one or all pad(s) a given colour
        The pad(s) will either revert to old colour or stay on the new one depending on the pulse_count value
        Odd: keep new colour, Even: keep previous colour. Exception: 0x00 keeps new colour.
        Pulse counts from 0xff will flash forever.
        Pad numbering: 0:All, 1:Center, 2:Left, 3:Right
        Colour values are 0-255, with 0 being off and 255 being maximum
        Colour should be a tuple of 0-255 values in the format (red, green,blue)
        Abstraction for command: 0x09 0xc3
        """
        red, green, blue = colour[0], colour[1], colour[2]
        command = [0x55, 0x09, 0xc3, 0x1f, pad, on_length, off_length, pulse_count, red, green, blue]
        self.send_command(command)
        return

    def fade_pad(self, pad, pulse_time, pulse_count, colour):
        """
        Fade one or all pad(s) a given colour with optional pulsing effect
        The pad(s) will either revert to old colour or stay on the new one depending on the pulse_count value
        Odd: keep new colour, Even: keep previous colour. Exception: 0x00 keeps new colour.
        pulse_count values of 0x00 and above 0x199 will flash forever.
        pulse_time starts fast at 0x01 and continues to 0xff which is very slow, 0x00 causes immediate change.
        Pad numbering: 0:All, 1:Center, 2:Left, 3:Right
        Colour values are 0-255, with 0 being off and 255 being maximum
        Colour should be a tuple of 0-255 values in the format (red, green,blue)
        Abstraction for command: 0x08 0xc2
        """
        red, green, blue = colour[0], colour[1], colour[2]
        command = [0x55, 0x08, 0xc2, 0x0f, pad, pulse_time, pulse_count, red, green, blue]
        self.send_command(command)
        return

    def switch_pads(self, *colours):
        """
        Requires 3 tuples:
            (Center),(Left),(Right)
        Each using the format:
            (R, G, B)
        Empty colour tuples will ignore that pad.
        Ignored pads will continue whatever they were doing previously.
        Abstraction for command: 0x0e 0xc8

        """
        assert(len(colours) == 3)
        command = [0x55, 0x0e, 0xc8, 0x06,]# Start of command
        for colour in colours:
            if len(colour) != 3:
                # Disable command for this pad
                enable = 0
                red, green, blue = 0, 0, 0
            else:
                # Send colour values for this pad
                enable = 1
                red, green, blue = colour[0], colour[1], colour[2]
            command += [enable, red, green, blue]# 3 identical segments, one for each colour
        self.send_command(command)
        return



def demo_switch_pads_skip(gateway):
    """
    Show how the previous effect on a pad is preverved with gateway.switch_pads()
    """
    print("Demonstrating ignore pad functionality in gateway.switch_pads()")
    # Test flash_pad()
    gateway.flash_pad(
        pad = 0,
        on_length = 10,
        off_length = 20,
        pulse_count = 100,
        colour = (255,0,0)# RGB
        )
    time.sleep(2)
    # test switch_pads()
    gateway.switch_pads(
        (255,0,0),# C:RGB
        (0,255,0),# L:RGB
        (),# R:skip
        )
    return


def debug():
    """
    For testing and debugging and coding and stuff
    """
    # Get gateway object
    gateway = Gateway(verbose=True)

    # Test switch_pad()
    gateway.switch_pad(
        pad=0,
        colour = (0, 255, 0)# RGB
        )

    time.sleep(10)
    gateway.blank_pads()
    time.sleep(1)

    # Test flash_pad()
    gateway.flash_pad(
        pad = 0,
        on_length = 10,
        off_length = 20,
        pulse_count = 100,
        colour = (255,0,0)# RGB
        )

    time.sleep(10)
    gateway.blank_pads()
    time.sleep(1)

    # Test fade_pad()
    gateway.fade_pad(
        pad = 1,
        pulse_time = 10,
        pulse_count = 10,
        colour = (255, 0, 255)# RGB
        )

    time.sleep(10)
    gateway.blank_pads()
    time.sleep(1)

    # test switch_pads()
    gateway.switch_pads(
        (255,0,0),# C:RGB
        (0,255,0),# L:RGB
        (),# R:skip
        )

    gateway.blank_pads()
    time.sleep(1)
    demo_switch_pads_skip(gateway)
    return


def main():
    debug()
    pass

if __name__ == '__main__':
    main()
