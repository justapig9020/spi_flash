from cmd import *
from spidev import *
from time import *

def is_set_flag (reg, flag):
    return reg & flag == flag

def get_jid (mem):
    return send_cmd (mem, RJID, 3)

def set_reg (mem, cmd, val):
    send_buf = []
    send_buf += [cmd]
    send_buf += [val]
    mem.xfer (send_buf)

def get_reg (mem, cmd):
    return send_cmd (mem, cmd, 1)[0]

def send_cmd(mem, cmd, ret_size):
    send_buf = []
    send_buf += [cmd]
    for i in range (ret_size):
        send_buf += [NOP]
    ret = mem.xfer (send_buf)
    ret.pop (0)
    return ret

def set_write_enable (mem):
    while True:
        sr1 = get_reg (mem, RSR1)
        if is_set_flag (sr1, SR1_BUSY) == False:
            break;
        sleep (1)

    for i in range (1000):
        mem.xfer ([WEN])
        sr1 = get_reg (mem, RSR1) 
        if is_set_flag (sr1, SR1_WEL):
            return True
        sleep (1)
    return False

def erase (mem, addr):
    if set_write_enable (mem) == False:
        return False

    send_buf = [SE]
    send_buf += addr
    mem.xfer (send_buf)
    return True

def write (mem, addr, data):
    if set_write_enable (mem) == False:
        return False
    
    send_buf = [PP]
    send_buf += addr
    send_buf += data
    mem.xfer (send_buf)
    return True

def read (mem, addr, size):
    for i in range (1000):
        mem.xfer ([WDI])
        sr1 = get_reg (mem, RSR1) 
        if is_set_flag (sr1, SR1_WEL | SR1_BUSY) == False:
            break
        # mem.xfer ([WDI])
        sleep (1)

    if is_set_flag (sr1, SR1_WEL | SR1_BUSY):
        return [0x00]
    else:
        send_buf = [RD]
        send_buf += addr
        for i in range (size):
            send_buf += [NOP]

        recv_buf = mem.xfer (send_buf)
        for i in range (4):
            recv_buf.pop(0)
    return recv_buf       
