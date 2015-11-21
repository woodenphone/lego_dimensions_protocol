#-------------------------------------------------------------------------------
# Name:        library
# Purpose:
#
# Author:      User
#
# Created:     21/11/2015
# Copyright:   (c) User 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------







class Gateway():
    """
    Represents a Lego Dimensions gateway/portal peripheral
    """
    def __init__(self):
        # Initialise USB connection to the device
        self.dev = self._init_usb()
        return

    def _init_usb(self):
        import usb.core
        import usb.util
        """
        Connect to and initialise the portal
        """
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


    def fade_pads(self,
        pad_1_enable,pad1_speed, pad1_red,
        pad2,
        pad3):
        """
        """
        return


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
    # Test fade_pads(


def main():
    debug()
    pass

if __name__ == '__main__':
    main()
