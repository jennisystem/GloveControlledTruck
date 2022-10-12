# A collection of utilites for the Feather M4 for EE11SC

import board
import busio
import sdcardio
import storage
import os

# mount the sd card on a Feather M4, assuming the chip select is D4
def mount_sd():

    # set up the SPI bus, and use D4 for chip select
    spi = board.SPI()
    cs = board.D4

    # open the card up, and mount it as a file system
    sdcard = sdcardio.SDCard(spi,cs)
    vsf = storage.VfsFat(sdcard)
    storage.mount(vfs,"/sd")
    return

# a utility to print a file
def print_file(fn):
    with open(fn,"r") as f:
        for line in f:
	    print(line,end='')
    return# Write your code here :-)
