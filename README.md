# SPI device module

## introduction
-   SPI device object class for winbond W25Q32JV series devices
-   Implement basic operatings included erase, read, write, reset etc.
-   For device feature execute erase the address before writing it
-   The erase command will erase entire sector 
    (256 bytes from argumented address with 0xFFFF00 bit mask) to 0xFF
