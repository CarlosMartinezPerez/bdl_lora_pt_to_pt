from machine import Pin, SPI
from time import sleep

cs  = Pin(17, Pin.OUT, value=1)
rst = Pin(28, Pin.OUT, value=1)
dio0= Pin(20, Pin.IN)

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

# imprimir versão
print("Versão:", hex(read_reg(0x42)))

# colocar frequency 915.0 MHz
write_reg(0x06, 0xE4)   # MSB
write_reg(0x07, 0xC0)   # MID
write_reg(0x08, 0x00)   # LSB

# modo RX contínuo LoRa
write_reg(0x01, 0x85)

print("SERVER raw 915MHz ouvindo IRQ...")

while True:
    if dio0.value() == 1:
        print("IRQ RECEBIDO")
    sleep(0.1)
