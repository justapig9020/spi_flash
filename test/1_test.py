from init import *
from ins import *

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

    print ("Read from: ", addr, " size: ", len(data))
    ret = read (mem, addr, len(data))
    prt_ret (ret)

    if erase (mem, addr) == False:
        print ("erase error", end=" ")
        return False

    print ("Read from: ", addr, " size: ", len(data))
    ret = read (mem, addr, len(data))
    prt_ret (ret)

    if write (mem, addr, data):
        print ("Read from: ", addr, " size: ", len(data))
        ret = read (mem, addr, len (data))
        prt_ret (ret)
        if ret != data:
            print ("R/W value not match")
            print (ret)
            return False
        
        addr[2] += 128
        ret = read (mem, addr, len (data))
        prt_ret (ret)

    else:
        print ("write error", end=" ")
    return True

mul_sel = gpiozero.LED (23)
mul_sel.off ()

mem = mem_init ()

addr = [0x00, 0x00, 0x00]
data = []
for i in range (256):
    data += [i]
# data = [0x09, 0x05, 0x02, 0x07]
test_func (mem, addr, data)

mem.close ()
