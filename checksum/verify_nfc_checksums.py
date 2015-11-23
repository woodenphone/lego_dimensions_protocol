#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      User
#
# Created:     23/11/2015
# Copyright:   (c) User 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os


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


def generate_checksum_from_valid_packet(packet):
    """Given a packet, generate the checksum for it.
    This function is intended for sniffed packets.
    Also to make sure we knwo how to calculate valid checksums.
    """
    assert(len(packet) is 32)
    print("packet: "+repr(packet))
    # Remove trailing zeros (if any)
    position = 0
    last_non_zero_position = 0
    for cropword in packet:
        position += 1
        if cropword != 0x00:
            last_non_zero_position = position

    if last_non_zero_position == 32:
        # Handle unpadded packets
        no_trailing_zeros = packet[:]
    else:
        # Remove padding
        no_trailing_zeros = packet[:last_non_zero_position]

    # Remove last byte (checksum)
    command = no_trailing_zeros[:-1]
    expected = no_trailing_zeros[-1]

    # Compute checksum
    result = generate_checksum_for_command(command)
    print("result: "+repr(result))
    if (result == expected) or (result == 0):
        return result
    else:
        print("locals():"+repr(locals()))
        assert(False)


def convert_to_byte_list(packet_line_string):
    """
    Take line from usb-mitm stdout and make it into a python libusb statement
    01[32]: 55 14 c6 16 01 1e 01 ff 00 18 01 1e 01 ff 00 18 01 1e 01 ff 00 18 ea 00 00 00 00 00 00 00 00 00
    becomes
    """
    packet_byte_strings = packet_line_string.split(" ")[1:]
    bytelist = []
    for packet_byte_string in packet_byte_strings:
        bytelist += [int(packet_byte_string, 16)]
    return bytelist


input_file_path = os.path.join("..","logs", "2015-11-16_with_known_led_commands_removed.log")

raw_output_dir = os.path.join("binned_log", "nfc_raw")
if not os.path.exists(raw_output_dir):
    os.makedirs(raw_output_dir)

with open(input_file_path, "r") as input_file:
    for line in input_file:
        if "[32]" not in line:# All USB endpoints for the device take 32-byte packets
            continue
        #81[32]: 55 01 15 6b 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        endpoint_number = line.split("[")[0]
        byte_strings = line.split(" ")[1:]
        command = "0x"+byte_strings[1]+"_0x"+byte_strings[2]
        # Isolate the command before the checksum
        bytelist = convert_to_byte_list(line[:-1])
        # Compare expected to actual checksums
        #print(bytelist)
        expected_checksum = generate_checksum_from_valid_packet(bytelist)





def main():
    pass

if __name__ == '__main__':
    main()
