import spidev
import cmd as spi_cmd
import time

default_speed = 31250000
default_mode = 0
default_delay = 0.001

def is_set_flag(reg, flag):
    return reg & flag == flag

class spi_flash:
    mem = spidev.SpiDev()
    delay = None
    bus = None
    dev_num = None

    def __init__(self, bus, dev_num, speed=default_speed, mode=default_mode, delay=default_delay):
        self.bus = bus
        self.dev_num = dev_num
        self.mem.open(self.bus, self.dev_num)
        self.setup(speed, mode, delay)

    def setup(self, speed=default_speed, mode=default_mode, delay=default_delay):
        self.mem.max_speed_hz = speed
        self.mem.mode = mode
        self.delay = delay
    
    def prt_status(self):
        print ("== SPI flash status ==")
        print ("Bus: %d, Dev: %d"%(self.bus, self.dev_num))
        print ("Speed: %dhz"%self.mem.max_speed_hz)
        print ("mode: %d"%self.mem.mode)
        print ("delay: %f"%self.delay)
        print ("======================")

    def read(self, addr, size):
        for i in range(10):
            self.mem.xfer([spi_cmd.WDI])
            sr1 = self.get_reg(spi_cmd.RSR1) 
            if is_set_flag(sr1, spi_cmd.SR1_WEL | spi_cmd.SR1_BUSY) == False:
                break
            time.sleep(self.delay)

        if is_set_flag(sr1, spi_cmd.SR1_WEL | spi_cmd.SR1_BUSY):
            return [0x00]
        else:
            send_buf = [spi_cmd.RD]
            send_buf += addr
            for i in range(size):
                send_buf += [spi_cmd.NOP]

            recv_buf = self.mem.xfer(send_buf)
            for i in range(4):
                recv_buf.pop(0)
        return recv_buf

    def get_jid(self):
        return self.send_cmd(self.mem, spi_cmd.RJID, 3)

    def chk_dev(self):
        ret = self.get_jid()
        mid = ret.pop(0)
        jid = ret
        return mid == 0xEF and jid == [0x40, 0x16]

    def set_reg(self, cmd, val):
        self.mem.xfer(spi_cmd.WENVSR)
        send_buf = [cmd]
        send_buf += [val]
        self.mem.xfer(send_buf)

    def get_reg(self, cmd):
        return self.send_cmd(self.mem, cmd, 1)[0]

    def send_cmd(self, mem, cmd, ret_size):
        send_buf = []
        send_buf += [cmd]
        for i in range(ret_size):
            send_buf += [spi_cmd.NOP]
        ret = self.mem.xfer(send_buf)
        ret.pop(0)
        return ret


    def set_write_enable(self):
        while True:
            sr1 = self.get_reg(spi_cmd.RSR1)
            if is_set_flag(sr1, spi_cmd.SR1_BUSY) == False:
                break;
            time.sleep(self.delay)

        for i in range(10):
            self.mem.xfer([spi_cmd.WEN])
            sr1 = self.get_reg(spi_cmd.RSR1) 
            if is_set_flag(sr1, spi_cmd.SR1_WEL):
                return True
            time.sleep(self.delay)
        return False


    def write(self, addr, data):
        if self.set_write_enable() == False:
            return False
    
        send_buf = [spi_cmd.PP]
        send_buf += addr
        send_buf += data
        self.mem.xfer(send_buf)
        return True

    def erase(self, addr):
        if self.set_write_enable() == False:
            return False

        send_buf = [spi_cmd.SE]
        send_buf += addr
        self.mem.xfer(send_buf)
        return True

        mem.close()
    def reset(self):
        self.mem.xfer([0x66])
        self.mem.xfer([0x99])

    def close(self):
        self.mem.close()
