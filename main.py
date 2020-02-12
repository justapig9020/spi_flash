import spi_flash

mem = spi_flash(0, 0)
mem.write (0x123456, 10)
