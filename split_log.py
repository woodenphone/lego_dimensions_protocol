#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      User
#
# Created:     14/11/2015
# Copyright:   (c) User 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

# Gather data
input_file = open("usb.log","ru")

endpoint_bins = {}# { "01" : [ [0x55,...], ...] }
previous_byte_string_list = None
previous_byte_list = None


for line in input_file:
    line = line.lower()# Fuck case sensitivity
    if line[2] == u"[":
        #01[32]: 55 14 c6 11 01 1e 01 ff 00 00 01 1e 01 ff 00 00 01 1e 01 ff 00 00 9d 00 00 00 00 00 00 00 00 00
        endpoint = line[:2]# "01"
        data_string = line.split(": ")[-1]# "55 14 c6 11 01 1e 01 ff 00 00 01 1e 01 ff 00 00 01 1e 01 ff 00 00 9d 00 00 00 00 00 00 00 00 00"
        byte_string_list = data_string.split(" ")# ["55",...]
        print "byte_string_list: "+repr(byte_string_list)

        byte_list = []
        for byte_string in byte_string_list:
            byte_list.append(int(byte_string, 16))
        print "byte_list: "+repr(byte_list)

        if endpoint == "01":
            assert(byte_string_list[0] == "55")# Byte 0 always 0x55
            assert(byte_string_list[1] == "14")# Byte 1 always 0x14
            assert(byte_string_list[2] == "c6")# Byte 2 always 0xc6

            if previous_byte_list is not None:# Byte 3 looks like a counter
                expected_byte_3_value = previous_byte_list[3]+1
                assert(byte_list[3] == expected_byte_3_value)

            # Byte 3 looks like a counter


# Parse data



def main():
    pass

if __name__ == '__main__':
    main()
