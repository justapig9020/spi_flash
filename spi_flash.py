import cmd.py
import spidev

class spi_flash:
    def __init__(self, bus, dev_num):
        self.spi_dev = spidev.SpiDev ()
        self.spi_dev.open (bus, dev_num);
    
    def read(addr, size):
        # read

    def write(addr, size):
        #write
