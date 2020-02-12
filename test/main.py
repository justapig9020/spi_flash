from spi_flash import spi_flash
import gpiozero

a = gpiozero.LED(23)
a.off()
mem = spi_flash(0, 0)
if mem.write([0x1f, 0x00, 0x00], [0x09, 0x05, 0x02, 0x07]):
    print(mem.read([0x1f, 0x00, 0x00],4))


