#-------------------------------------------------------------------------------
# Name:        bin_putty_log
# Purpose:    Collect USB packets sent to lego dimensions portal from log of putty
#               session and sort by endpoint and (hopefully) command id byte
#
# Author:      User
#
# Created:     17/11/2015
# Copyright:   (c) User 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os



def pythonify_packet(packet_line_string):
    """
    Take line from usb-mitm stdout and make it into a python libusb statement
    01[32]: 55 14 c6 16 01 1e 01 ff 00 18 01 1e 01 ff 00 18 01 1e 01 ff 00 18 ea 00 00 00 00 00 00 00 00 00
    becomes
    dev.write(1, [0x55, 0x06, 0xc0, 0x02, 0x00, 0xff, 0xff, 0xff, 0x1a, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])# Switch to blue
    """
    endopint = packet_line_string.split("[")[0]
    packet_byte_strings = packet_line_string.split(" ")[1:]
    formatted_packet_bytes = "["
    for packet_byte_string in packet_byte_strings:
        formatted_packet_bytes += "0x"+packet_byte_string+", "
    formatted_packet_bytes = formatted_packet_bytes[:-2]
    formatted_packet_bytes += "]"
    statement = "dev.write("+endopint+", "+formatted_packet_bytes+")"
    print statement
    return statement





input_file_path = os.path.join("logs", "2015-11-16_play_game_fo_a_while_putty.log")
output_dir = os.path.join("binned_log")
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


with open(input_file_path, "r") as input_file:
    for line in input_file:
        if "[32]" not in line:# All USB endpoints for the device take 32-byte packets
            continue
        #81[32]: 55 01 15 6b 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        endpoint_number = line.split("[")[0]
        byte_strings = line.split(" ")[1:]
        command = byte_strings[1]
        output_file_name = endpoint_number+"_"+command+".txt"
        output_file_path = os.path.join(output_dir, output_file_name)
        with open(output_file_path, "a") as output_file:
            output_file.write(line)
        expression = pythonify_packet(line[:-1])
        expression_output_file_name = endpoint_number+"_"+command+".py"
        expression_output_file_path = os.path.join(output_dir, expression_output_file_name)
        with open(expression_output_file_path, "a") as expression_output_file:
            expression_output_file.write(expression+"\n")







def main():
    pass

if __name__ == '__main__':
    main()
