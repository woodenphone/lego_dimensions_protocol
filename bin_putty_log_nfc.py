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
import os

input_file_path = os.path.join("logs", "2015-11-16_play_game_fo_a_while_putty.log")

raw_output_dir = os.path.join("binned_log", "nfc_raw")
if not os.path.exists(raw_output_dir):
    os.makedirs(raw_output_dir)

with open(input_file_path, "r") as input_file:
    for line in input_file:
        if "[32]" not in line:# All USB endpoints for the device take 32-byte packets
            continue
        if """04 9A 74 6A 0B 40 80""".lower() not in line.lower():
            continue
        #81[32]: 55 01 15 6b 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        endpoint_number = line.split("[")[0]
        byte_strings = line.split(" ")[1:]
        command = "0x"+byte_strings[1]+"_0x"+byte_strings[2]
        # Save raw
        output_file_name = endpoint_number+"_"+command+".txt"
        output_file_path = os.path.join(raw_output_dir, output_file_name)
        with open(output_file_path, "a") as output_file:
            output_file.write(line)


def main():
    pass

if __name__ == '__main__':
    main()

