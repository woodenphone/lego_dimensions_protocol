This project is currently focused on working out the communications protocol used.
The LED control commands appear to be deciphered.
A python library for controling the gateway device's lights is provided. (lego_dimensions_gateway.py)

The Xbox variant of the portal is not supported.

Windows installation:
Make sure the latest python 2.x is installed.
http://www.ninite.com is an easy way to install python.

Install LibUSB 
Open the start menu
In the search box at the bottom, type "command"
Click on "Command Prompt" result which will appear at the top
Copy the following command and then right click in the command prompt window and select "Paste"
"C:\Python27\Scripts\pip install pyusb"
You now have the python bindings for libusb installed, but there is still more that needs doing.

Download libusb-win32 and extract it. http://sourceforge.net/projects/libusb-win32/
Find if you are using a 32bit(x86) or 64bit(x64 A.K.A. amd64) computer.
open the bin/ folder.
Open the folder that matches your computer.
Plug in the USB portal device.
Run install-filter-win.exe
Make sure "Install a device filter" is selected.
Click next.
You will be given a list of USB devices.
Choose the LEGO one.
It will go back to the device selection screen after it installs
Now that it does not have any option for a LEGO device, click "Cancel" to exit the installer.

Run "morse.py" to test that everything worked.
If the pads on the gateway portal device begin flashing, you have succeeded in installing everything.


Linux and MacOS documentation is not provided at this time.


