import spidev 
import gpiozero
from cmd import *
from time import *

class spi_flash:
    mem = spidev.SpiDev()
    def __init__(self, bus, dev_num):
        self.bus = bus
        self.dev_num = dev_num

    def mem_init(self):
        self.mem = spidev.SpiDev()
        self.mem.open(self.bus, self.dev_num)
        self.mem.max_speed_hz = 1000000
        self.mem.mode = 0

    def read(self, addr, size):
        for i in range (1000):
            self.mem.xfer ([WDI])
            sr1 = self.get_reg (self.mem, RSR1) 
            if self.is_set_flag (sr1, SR1_WEL | SR1_BUSY) == False:
                break
            sleep (1)

        if self.is_set_flag (sr1, SR1_WEL | SR1_BUSY):
            return [0x00]
        else:
            send_buf = [RD]
            send_buf += addr
            for i in range (size):
                send_buf += [NOP]

            recv_buf = self.mem.xfer (send_buf)
            for i in range (4):
                recv_buf.pop(0)
        return recv_buf

    def is_set_flag (self, reg, flag):
        return reg & flag == flag

    def get_jid (self):
        return self.send_cmd (self.mem, RJID, 3)

    def check_id(self):
        ret = self.get_jid()
        print(ret)
        mid = ret.pop(0)
        jid = ret
        print("mid", hex(mid))
        for i in jid:
            print(hex(i))

        if mid != 0xef:
            print("send error")
            return False

    def set_reg (self, cmd, val):
        send_buf = []
        send_buf += [cmd]
        send_buf += [val]
        self.mem.xfer (send_buf)

    def get_reg (self, mem, cmd):
        return self.send_cmd (mem, cmd, 1)[0]

    def send_cmd(self, mem, cmd, ret_size):
        send_buf = []
        send_buf += [cmd]
        for i in range (ret_size):
            send_buf += [NOP]
        ret = self.mem.xfer (send_buf)
        ret.pop (0)
        return ret


    def set_write_enable (self):
        while True:
            sr1 = self.get_reg (self.mem, RSR1)
            if self.is_set_flag (sr1, SR1_BUSY) == False:
                break;
            sleep (1)

        for i in range (1000):
            self.mem.xfer ([WEN])
            sr1 = self.get_reg (self.mem, RSR1) 
            if self.is_set_flag (sr1, SR1_WEL):
                return True
            sleep (1)
        return False


    def write (self, addr, data):
        if self.set_write_enable () == False:
            return False
    
        send_buf = [PP]
        send_buf += addr
        send_buf += data
        self.mem.xfer (send_buf)
        return True

    def erase (self, addr):
        if self.set_write_enable () == False:
            return False

        send_buf = [SE]
        send_buf += addr
        self.mem.xfer (send_buf)
        return True


    def reset(self):
        self.mem.xfer([0x66])
        self.mem.xfer([0x99])
        self.mem.xfer([0x9f, 0x00, 0x00,0x00])
