import spidev 
from cmd import *
from time import *

def is_set_flag(reg, flag):
    return reg & flag == flag

class spi_flash:
    mem = spidev.SpiDev()
    delay = 0.5

    def __init__(self, bus, dev_num, speed = 1000000, mode = 0):
        self.bus = bus
        self.dev_num = dev_num
        self.mem.open(self.bus, self.dev_num)
        self.setup(speed, mode)

    def setup(self, speed=1000000, mode=0):
        self.mem.max_speed_hz = speed
        self.mem.mode = mode

    def read(self, addr, size):
        for i in range(10):
            self.mem.xfer([WDI])
            sr1 = self.get_reg(self.mem, RSR1) 
            if self.is_set_flag(sr1, SR1_WEL | SR1_BUSY) == False:
                break
            sleep(self.delay)

        if is_set_flag(sr1, SR1_WEL | SR1_BUSY):
            return [0x00]
        else:
            send_buf = [RD]
            send_buf += addr
            for i in range(size):
                send_buf += [NOP]

            recv_buf = self.mem.xfer(send_buf)
            for i in range(4):
                recv_buf.pop(0)
        return recv_buf

    def get_jid(self):
        return self.send_cmd(self.mem, RJID, 3)

    def chk_dev(self):
        ret = self.get_jid()
        mid = ret.pop(0)
        jid = ret
        return mid == 0xEF && jid == [0x40, 0x16]

    def set_reg(self, cmd, val):
        self.mem.xfer(WENVSR)
        send_buf = [cmd]
        send_buf += [val]
        self.mem.xfer(send_buf)

    def get_reg(self, cmd):
        return self.send_cmd(self.mem, cmd, 1)[0]

    def send_cmd(self, mem, cmd, ret_size):
        send_buf = []
        send_buf += [cmd]
        for i in range(ret_size):
            send_buf += [NOP]
        ret = self.mem.xfer(send_buf)
        ret.pop(0)
        return ret


    def set_write_enable(self):
        while True:
            sr1 = self.get_reg(self.mem, RSR1)
            if is_set_flag(sr1, SR1_BUSY) == False:
                break;
            sleep(self.delay)

        for i in range(10):
            self.mem.xfer([WEN])
            sr1 = self.get_reg(self.mem, RSR1) 
            if is_set_flag(sr1, SR1_WEL):
                return True
            sleep(self.delay)
        return False


    def write(self, addr, data):
        if self.set_write_enable() == False:
            return False
    
        send_buf = [PP]
        send_buf += addr
        send_buf += data
        self.mem.xfer(send_buf)
        return True

    def erase(self, addr):
        if self.set_write_enable() == False:
            return False

        send_buf = [SE]
        send_buf += addr
        self.mem.xfer(send_buf)
        return True

    def reset(self):
        self.mem.xfer([0x66])
        self.mem.xfer([0x99])
