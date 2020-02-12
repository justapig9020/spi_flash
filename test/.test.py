from init import *
from time import *

"""
def send (mem):
    mem.xfer ([0x06])
    sr1 = mem.xfer ([0x05, 0x00])[1]
    while sr1 & 0x02 != 0x02:
        print ("WR_EN failed")
        sleep (1)
        mem.xfer ([0x04])
        mem.xfer ([0x06])
        sr1 = mem.xfer ([0x05, 0x00])[1]

    if sr1 & 0x02:
        mem.xfer ([0x02, 0x00, 0x00, 0x00, 0x01, 0x02, 0x03])
        ret = mem.xfer ([0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        if ret == [0x00, 0x00, 0x00, 0x00, 0x01, 0x02, 0x03]:
            print ("success!")
            return True
        else:
            print ("R/W failed" + str (ret))
            return False 
    else:
        print ("WR_EN failed")
        return False

mul_sel = gpiozero.LED (23)
mul_sel.off ()
mem = init ()
mem.max_speed_hz = 33333000

while mem.max_speed_hz > 0:
    print ("==== clk:" + str(mem.max_speed_hz) + " ====")
    sd_ret = send (mem)
    if sd_ret:
        break
    mem.max_speed_hz = mem.max_speed_hz - 1000
"""
