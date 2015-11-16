#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      User
#
# Created:     15/11/2015
# Copyright:   (c) User 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import scapy.all
import os

capture_path = os.path.join("logs", "2015-11-15_turn_on_and_leave_unattended_at_start_screen.pcap")
a = scapy.rdpcap(capture_path)





def main():
    pass

if __name__ == '__main__':
    main()
