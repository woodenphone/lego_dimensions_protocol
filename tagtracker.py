#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      User
#
# Created:     23/11/2015
# Copyright:   (c) User 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import usb
import usb.core
import usb.util
import time
import threading



class TagTracker():
    """
    Keep track of where pads are on the pad
    """
    USB_read_timeout = 10 # 10 ms seems okay for the demo
    _USB_thread = None
    _tag_locations = {
        "removed":set(),
        1:set(),
        2:set(),
        3:set(),
        }
    def __init__(self,verbose=True):
        self.verbose = verbose
        # Initialise USB connection to the device
        self.dev = self._init_usb()
        # Reset the state of the device to all pads off
        #self.blank_pads()
        # Begin watching USB in a new thread
        self._USB_thread = threading.Thread(target=self._usb_read_thread,
            args=())
        self._USB_thread.start()
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

    def _remove_tag(self, tag_uid):
        # Remove tag from all
        for pad_id in self._tag_locations.keys():
            self._tag_locations[pad_id].discard(tag_uid)
        # Add to removed box
        self._tag_locations["removed"].add(tag_uid)
        return

    def _add_tag(self, tag_uid, destination):
        # Remove tag from all
        for pad_id in self._tag_locations.keys():
            self._tag_locations[pad_id].discard(tag_uid)
        # Add to new
        self._tag_locations[destination].add(tag_uid)
        return

    def locate_tag(self, tag_uid):
        """Return the position of a specified tag"""
        for pad_id in self._tag_locations.keys():
            if tag_uid in self._tag_locations[pad_id]:
                return pad_id
        # If we don't know
        self._remove_tag(self, tag_uid)
        return None

    def list_tags(self):
        """Return a list of the tags currently being tracked"""
        tags = []
        for pad_id in self._tag_locations.keys():
            tags += list(self._tag_locations[pad_id])
        return tags

    def stringify_uid(self,uid_bytes):
        """Convert the bytes for the UID into a string so we can put it into a set"""
        uid = ""
        for uid_byte in uid_bytes:
            uid += str(uid_byte)
        return uid

    def _update_nfc(self):
        try:
            inwards_packet = self.dev.read(0x81, 32, timeout = self.USB_read_timeout)
            #print("inwards_packet:"+repr(inwards_packet))
            bytelist = list(inwards_packet)
            #print("bytelist:"+hex_repr(bytelist))

            if not bytelist:# We need a packet
                return
            if bytelist[0] != 0x56:# Only listen to NFC packets
                return

            pad_num = bytelist[2]
            uid_bytes = bytelist[6:12]
            uid = self.stringify_uid(uid_bytes)
            removed = bool(bytelist[5])# Was the tag removed, if false it was added
            if removed:
                self._remove_tag(tag_uid=uid)
            else:
                self._add_tag(tag_uid=uid, destination=pad_num)
        except usb.USBError, err:
            pass

    def _usb_read_thread(self):
        while True:
            self._update_nfc()


def watch_pads():
    """Demo, tracks tag locations and prints them"""
    tracker = TagTracker()
    while True:
        time.sleep(0.5)
        tags = tracker.list_tags()
        if tags:
            print("")# Seperator between text blocks
        for tag in tags:
            tag_location = tracker.locate_tag(tag)
            if tag_location == "removed":
                print("tag:"+repr(tag)+" has been removed from the gateway")
            else:
                print("tag:"+repr(tag)+" is located on pad "+repr(tag_location))
    return


def main():
    watch_pads()

if __name__ == '__main__':
    main()
