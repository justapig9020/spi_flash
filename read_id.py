#!/usr/bin/python3
# ref:
#
import cmd
import spidev


  # bus, or called channel
bus=0
  # which CS?  (CS0 or CS1)
csid=0

# initial
dev = spidev.SpiDev ()

# setup
dev.open(bus, csid)
print("speed = ", dev.max_speed_hz)
print("bits_per_word = ", dev.bits_per_word)


# xfer([...], speed, delay_us, bits_per_word)
result = dev.xfer([0x9f, 0, 0, 0], 1000000, 0, 0)

print("Get ID in 1M speed = ", end="")
for i in result:
    print (hex (i), end=" ")
print ()

result = dev.xfer([0x9f, 0, 0, 0], 125000000, 0, 0)
print("Get ID in 125M? speed = ", end="")
for i in result:
    print (hex (i), end=" ")
print ()

