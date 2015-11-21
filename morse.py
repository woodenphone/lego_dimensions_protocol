#-------------------------------------------------------------------------------
# Name:        morse
# Purpose:  Demo of the gateway library
#
# Author:      User
#
# Created:     21/11/2015
# Copyright:   (c) User 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import time
import library
import re


TIME_UNIT = 0.2# Base time unit in seconds
DASH = TIME_UNIT*3
DOT = TIME_UNIT*1
SPACE = TIME_UNIT*3

# codes transcribed from picture on http://thelivingpearl.com/2013/01/08/morse-code-and-dictionaries-in-python-with-sound/
MORSE_CODE_TABLE = {
    "a":".-",
    "b":"-...",
    "c":"-.-.",
    "d":"-..",
    "e":".",
    "f":"..-.",
    "g":"--.",
    "h":"....",
    "i":"..",
    "j":".---",
    "k":"-.-",
    "l":".-..",
    "m":"--",
    "n":"-.",
    "o":"---",
    "p":".--.",
    "q":"--.-",
    "r":".-.",
    "s":"...",
    "t":"-",
    "u":"..-",
    "v":"...-",
    "w":".--",
    "x":"-..-",
    "y":"-.--",
    "z":"--..",

    "0":"-----",
    "1":".----",
    "2":"..---",
    "3":"...--",
    "4":"....-",
    "5":".....",
    "6":"-....",
    "7":"--...",
    "8":"---..",
    "9":"----.",
    }




def send_character(gateway, character):
    character = character.lower()
    print(character)
    if character == " ":
        time.sleep(SPACE)
    else:
        code = MORSE_CODE_TABLE[character]
        for symbol in code:
            # Flash for appropriate time
            if symbol == ".":
                gateway.switch_pad(
                    pad = 0,
                    red = 255,
                    green = 0,
                    blue = 0
                    )
                time.sleep(DOT)
            elif symbol == "-":
                gateway.switch_pad(
                    pad = 0,
                    red = 0,
                    green = 0,
                    blue = 255
                    )
                time.sleep(DASH)
            # Turn pad back off
            gateway.switch_pad(
                pad = 0,
                red = 0,
                green = 0,
                blue = 0
                )
            time.sleep(TIME_UNIT)
    return

def send_text(gateway, text):
    clean_text = re.sub("[^a-z0-9 ]","", text.lower())
    for character in clean_text:
        send_character(gateway, character)
    return


def main():
    text = "Lego Dimensions gateway morse code demonstration"
    gateway = library.Gateway()
    send_text(gateway, text)

if __name__ == '__main__':
    main()
