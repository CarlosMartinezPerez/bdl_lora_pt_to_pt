from machine import Pin, SPI

# pinos SPI do LoRa RFM95W conforme seu mapeamento
cs  = Pin(17, Pin.OUT, value=1)
spi = SPI(0, baudrate=5000000, polarity=0, phase=0, bits=8,
          sck=Pin(18), mosi=Pin(19), miso=Pin(16))

def read_reg(addr):
    cs.off()
    spi.write(bytearray([addr & 0x7F])) # bit 7 = 0 para leitura
    res = spi.read(1)
    cs.on()
    return res[0]

ver = read_reg(0x42)
print("REG_VERSION =", hex(ver))
