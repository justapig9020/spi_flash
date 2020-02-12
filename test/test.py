from init import *
from ins import *

def set_sr3 (mem):
    sr3 = get_reg (mem, RSR3)
    print (hex (sr3))
    if False:
        send_buf = sr3 & ~(flag)
        print (hex (send_buf))
        send_cmd (mem, WENVSR, 0)
        set_reg (mem, WSR3, send_buf)

def prt_ret (ret):
    c = 0
    for i in ret:
        print (i, end="\t")
        if c & 0xf == 0xf:
            print ()
        c += 1
    print ()

def test_func (mem, addr, data):
    ret = get_jid (mem)
    mid = ret.pop (0)
    jid = ret
    print ("mid:", hex (mid))
    print ("jid:", end=" ")
    for i in jid: 
        print (hex (i), end=" ")
    print ()

    if mid != 0xef:
        print ("send error", end=" ")
        return False

    if erase (mem, addr) == False:
        print ("erase error", end=" ")
        return False

    ret = read (mem, addr, len(data))
    prt_ret (ret)

    if write (mem, addr, data):
        ret = read (mem, addr, len (data))
        prt_ret (ret)
        if ret != data:
            print (ret)
            return False
    else:
        print ("write error", end=" ")
    return True

def test_loop (mem, addr, data):
    print ("=== ", mem.max_speed_hz, " ===")
    if test_func (mem, addr, data):
        return
    else:
        print (" test failed")

flag = SR3_DRV1 | SR3_DRV2
addr = [0x1f, 0x00, 0x00]
# data = [0x01, 0x02, 0x03, 0x04]
data = [0x09, 0x05, 0x02, 0x07]

mem = mem_init ()

mem.max_speed_hz = 1000000 

#while mem.max_speed_hz > 0:
test_loop (mem, addr, data)
#    mem.max_speed_hz -= 1000

mem.close ()
