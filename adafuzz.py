import usb.core
import usb.util
import sys

# find our device
dev = usb.core.find(idVendor=0xE6f, idProduct=0x241)

# was it found?
if dev is None:
    raise ValueError('Device not found')

# set the active configuration. With no arguments, the first
# configuration will be the active one
dev.set_configuration()







### get an endpoint instance
##cfg = dev.get_active_configuration()
##intf = cfg[(0,0)]
##
##ep = usb.util.find_descriptor(
##    intf,
##    # match the first OUT endpoint
##    custom_match = \
##    lambda e: \
##        usb.util.endpoint_direction(e.bEndpointAddress) == \
##        usb.util.ENDPOINT_OUT)
##
##assert ep is not None
##print "got endpoint"
### write the data
##ep.write('test')



# Let's fuzz around!

# Lets start by Reading 1 byte from the Device using different Requests
# bRequest is a byte so there are 255 different values
for bRequest in range(256):
    try:
        #ctrl_transfer( bmRequestType, bmRequest, wValue, wIndex, nBytes)
        ret = dev.ctrl_transfer(0x00, bRequest, 0, 0, 1)
        print "bRequest ",bRequest
        print ret
    except:
        # failed to get data for this request
        pass