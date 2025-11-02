from machine import Pin, SPI
from time import sleep

cs  = Pin(17, Pin.OUT, value=1)
rst = Pin(28, Pin.OUT, value=1)
spi = SPI(0, baudrate=1000000, polarity=0, phase=0, bits=8, sck=Pin(18), mosi=Pin(19), miso=Pin(16))

def write_reg(addr, value):
    cs.off()
    spi.write(bytearray([addr | 0x80, value]))
    cs.on()

def read_reg(addr):
    cs.off()
    spi.write(bytearray([addr & 0x7F]))
    v = spi.read(1)
    cs.on()
    return v[0]

print("Versão:", hex(read_reg(0x42)))

# configurar mesma freq 915.0 MHz
write_reg(0x06, 0xE4)
write_reg(0x07, 0xC0)
write_reg(0x08, 0x00)

print("Transmitindo pulso TX a 915MHz...")

while True:
    write_reg(0x01, 0x83) # TX mode
    sleep(1)
