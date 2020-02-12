import cmd
import spidev

def get_byte(val, off):
    val = val >> (off * 8)
    val = val & 0xff
    return val

def is_flag_set(reg, flag):
    return (reg|flag) == flag

def set_wr_en(mem):
    mem.xfer([WREN])

def is_set_wel(mem):
    st_reg = mem.xfer([RDSR])
    return is_flag_set (st_reg, SR_WIP)
 
def wr_byte(addr, val):
    print (get_byte (addr, 2), get_byte (addr, 1), get_byte (addr, 0))
   # mem.xfer ([PP, get_byte (addr, 2), get_byte (addr, 1), get_byte (addr, 0), val])

class spi_flash:
    def __init__(self, bus, dev_num):
        self.dev = spidev.SpiDev ()
        self.dev.open (bus, dev_num);
        return self

    def read(addr):
        return 0

    def write(addr, val):
        #        set_wr_en(self.dev)
        #if is_set_wel (self.dev) == False:
        #    return False
        wr_byte (addr, val)       
