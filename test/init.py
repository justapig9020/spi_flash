import spidev
import gpiozero


def mem_init ():
    mem = spidev.SpiDev ()
    mem.open (0, 0)
    mem.max_speed_hz = 1000000
    mem.mode = 0
    return mem
