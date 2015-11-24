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
# EP  Cmd - func_name() - Description
# 01 0xc0 - switch_pad() - Immediately switch one or all pad(s) to a single value
# 01 0xc2 - fade_pad() - Immediately change the colour of one or all pad(s), fade and flash available
# 01 0xc3 - flash_pad() - set 1 or all pad(s) to a colour with variable flash rates
# 01 0xc8 - switch_pads() - Immediately switch pad(s) to set of colours
# 01 0xc6 - fade_pads() - Fade pad(s) to value(s)
# 01 0xc7 - flash_pads - Flash all 3 pads with individual colours and rates, either change to new or return to old based on pulse count


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
        Abstraction for command: 0xc0
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
        Abstraction for command: 0xc3
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
        Abstraction for command: 0xc2
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
        Abstraction for command: 0xc8

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

    def fade_pads(self, *pads):# TODO get second opinion on arguments
        """
        Fade pad(s) to value(s)
        Each pad is represented by a tuple in the format:
            (fade_time, pulse_count, (R,G,B) )
        Colour values must be from 0-255 (0x00-0xff)
        Empty colour tuples will ignore that pad.
        TODO investigate time values
        TODO investigate count values
        Abstraction for command: 0xc6

        """
        assert(len(pads) == 3)
        command = [0x55, 0x14, 0xc6, 0x26,]
        for pad in pads:
            if len(pad) != 3:
                # Disable command for this pad
                enable = 0
                fade_time = 0
                pulse_count = 0
                red, green, blue = 0, 0, 0
            elif len(pad[2]) != 3:
                # Disable command for this pad
                enable = 0
                fade_time = 0
                pulse_count = 0
                red, green, blue = 0, 0, 0
            else:
                # Enable pad for the command
                enable = 1
                colour = pad[2]
                red, green, blue = colour[0], colour[1], colour[2]
                fade_time = pad[0]
                pulse_count = pad[1]
            command += [enable, fade_time, pulse_count, red, green, blue]
            continue
        self.send_command(command)
        return


    def flash_pads(self, *pads):# TODO get second opinion on arguments
        """
        Flash all 3 pads with individual colours and rates, either change to new or return to old based on pulse count.
        Each pad is represented by a tuple in the format:
            (on_length, off_length, pulse_count, (R,G,B) )
        Colour values must be from 0-255 (0x00-0xff)
        Empty colour tuples will ignore that pad.
        Ignored pads will continue whatever they were doing previously.
        Empty colour tuples will ignore that pad.
        Ignored pads will continue whatever they were doing previously.

        On pulse length - 0x00 is almost impersceptible,  0xff is ~10 seconds
        Off pulse length - 0x00 is almost impersceptible, 0xff is ~10 seconds
        Number of flashes - odd value leaves pad in new colour, even leaves pad in old, except for 0x00, which changes to new. Values above 0xc6 dont stop.
        Abstraction for command: 0xc7
        """
        assert(len(pads) == 3)
        command = [0x55, 0x17, 0xc7, 0x3e,]
        for pad in pads:
            if len(pad) != 4:
                # Disable command for this pad
                enable = 0
                on_length = 0
                off_length = 0
                pulse_count = 0
                red, green, blue = 0, 0, 0
            elif len(pad[3]) != 3:
                # Disable command for this pad
                enable = 0
                on_length = 0
                off_length = 0
                pulse_count = 0
                red, green, blue = 0, 0, 0
            else:
                # Enable pad for the command
                enable = 1
                colour = pad[3]
                red, green, blue = colour[0], colour[1], colour[2]
                on_length = pad[0]
                off_length = pad[1]
                pulse_count = pad[2]
            command += [enable, on_length, off_length, pulse_count, red, green, blue]
            continue
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


def test_flash_pads(gateway):
    # test flash_pads()
    gateway.flash_pads(# 3 changing pads
        (5, 10, 15, (255,0,0)),# (on_length, off_length, pulse_count, (R,G,B) )
        (20, 25, 30, (0,255,0)),# (on_length, off_length, pulse_count, (R,G,B) )
        (35, 40, 45, (0,0,255)),# (on_length, off_length, pulse_count, (R,G,B) )
        )
    pause_between_tests(gateway)
    gateway.flash_pads(# Two ignored pads
        (5, 10, 15, ()),# On, off, count, (R,G,B)
        (),# On, off, count, (R,G,B)
        (5, 40, 10, (255,0,255)),# On, off, count, (R,G,B)
        )
    return


def test_fade_pads(gateway):
    # test fade_pads()
    gateway.fade_pads(# 3 changing pads
        (10, 20, (255, 0, 0)),# (fade_time, pulse_count, (R,G,B) )
        (20, 10, (0, 255, 0)),# (fade_time, pulse_count, (R,G,B) )
        (15, 15, (0, 0, 255)),# (fade_time, pulse_count, (R,G,B) )
        )
    pause_between_tests(gateway)
    gateway.fade_pads(# Two ignored pads
        (),# (fade_time, pulse_count, (R,G,B) )
        (20, 10, ()),# (fade_time, pulse_count, (R,G,B) )
        (15, 15, (0, 0, 255)),# (fade_time, pulse_count, (R,G,B) )
        )
    return


def pause_between_tests(gateway):
    time.sleep(10)
    gateway.blank_pads()
    time.sleep(1)


def debug():
    """
    For testing and debugging and coding and stuff
    """
    # Get gateway object
    gateway = Gateway(verbose=True)

    # Test functions for library
    #test_flash_pads(gateway)
    #pause_between_tests(gateway)

    test_fade_pads(gateway)
    return

    # Test switch_pad()
    gateway.switch_pad(
        pad=0,
        colour = (0, 255, 0)# RGB
        )

    pause_between_tests(gateway)

    # Test flash_pad()
    gateway.flash_pad(
        pad = 0,
        on_length = 10,
        off_length = 20,
        pulse_count = 100,
        colour = (255,0,0)# RGB
        )

    pause_between_tests(gateway)

    # Test fade_pad()
    gateway.fade_pad(
        pad = 1,
        pulse_time = 10,
        pulse_count = 10,
        colour = (255, 0, 255)# RGB
        )

    pause_between_tests(gateway)

    # test switch_pads()
    gateway.switch_pads(
        (255,0,0),# C:RGB
        (0,255,0),# L:RGB
        (),# R:skip
        )

    pause_between_tests(gateway)

    demo_switch_pads_skip(gateway)
    return


def main():
    debug()
    pass

if __name__ == '__main__':
    main()
