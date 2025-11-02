# client_packet.py
from machine import Pin, SPI
from time import sleep

# Pinos conforme sua pinagem
CS = Pin(17, Pin.OUT, value=1)
RESET = Pin(28, Pin.OUT, value=1)
spi = SPI(0, baudrate=1000000, polarity=0, phase=0, bits=8,
          sck=Pin(18), mosi=Pin(19), miso=Pin(16))

# registradores usados
REG_OP_MODE = 0x01
REG_FRF_MSB = 0x06
REG_FRF_MID = 0x07
REG_FRF_LSB = 0x08
REG_FIFO = 0x00
REG_FIFO_ADDR_PTR = 0x0D
REG_FIFO_TX_BASE = 0x0E
REG_PAYLOAD_LEN = 0x22
REG_IRQ_FLAGS = 0x12
REG_PA_CONFIG = 0x09
REG_PA_DAC = 0x4D

def spi_write_reg(addr, value):
    CS.off()
    spi.write(bytearray([addr | 0x80, value]))
    CS.on()

def spi_read_reg(addr):
    CS.off()
    spi.write(bytearray([addr & 0x7F]))
    v = spi.read(1)
    CS.on()
    return v[0]

# helper para escrever buffer no FIFO (usa burst write)
def fifo_write(data):
    CS.off()
    spi.write(bytearray([REG_FIFO | 0x80]) + data)
    CS.on()

# reset sequence
RESET.value(0)
sleep(0.01)
RESET.value(1)
sleep(0.01)

# confirma versão
ver = spi_read_reg(0x42)
print("REG_VERSION =", hex(ver))

# configurar frequência 915 MHz (valores já testados)
spi_write_reg(REG_FRF_MSB, 0xE4)   # 915 MHz MSB
spi_write_reg(REG_FRF_MID, 0xC0)
spi_write_reg(REG_FRF_LSB, 0x00)

# config modem: Bw125 Cr4/5 Sf128 (common)
spi_write_reg(0x1D, 0x72)  # RegModemConfig1
spi_write_reg(0x1E, 0x74)  # RegModemConfig2
spi_write_reg(0x26, 0x04)  # RegModemConfig3 (low datarate off)

# set FIFO pointers
spi_write_reg(REG_FIFO_TX_BASE, 0x00)
spi_write_reg(REG_FIFO_ADDR_PTR, 0x00)

# set PA config (use PA_BOOST)
spi_write_reg(REG_PA_DAC, 0x07)     # enable high power if desired
spi_write_reg(REG_PA_CONFIG, 0x80 | (14 - 2))  # PA_SELECT | (power-2) conservative

print("Transmitindo pacotes (payload curto) a cada 2s...")

count = 0
while True:
    payload = b"PING %d" % count
    count += 1

    # write payload to FIFO
    fifo_write(payload)

    # set payload length
    spi_write_reg(REG_PAYLOAD_LEN, len(payload))

    # set mode TX (LoRa, TX)
    spi_write_reg(REG_OP_MODE, 0x83)  # LONG_RANGE_MODE + MODE_TX

    # wait for TX done by polling IRQ register (optional)
    # aqui vamos apenas esperar um pouco e continuar
    sleep(0.6)

    # clear IRQ flags (just in case)
    spi_write_reg(REG_IRQ_FLAGS, 0xFF)

    print("enviado:", payload)
    sleep(1.4)
