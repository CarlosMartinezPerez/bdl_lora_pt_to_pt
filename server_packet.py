# server_packet.py
from machine import Pin, SPI
from time import sleep

CS = Pin(17, Pin.OUT, value=1)
RESET = Pin(28, Pin.OUT, value=1)
DIO0 = Pin(20, Pin.IN)   # DIO0 mapeado pra RXDONE
spi = SPI(0, baudrate=1000000, polarity=0, phase=0, bits=8,
          sck=Pin(18), mosi=Pin(19), miso=Pin(16))

REG_OP_MODE = 0x01
REG_FRF_MSB = 0x06
REG_FRF_MID = 0x07
REG_FRF_LSB = 0x08
REG_FIFO = 0x00
REG_FIFO_ADDR_PTR = 0x0D
REG_FIFO_RX_CURRENT_ADDR = 0x10
REG_RX_NB_BYTES = 0x13
REG_IRQ_FLAGS = 0x12
REG_FIFO_RX_BASE = 0x0F
REG_PAYLOAD_LEN = 0x22

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

def fifo_read(n):
    CS.off()
    spi.write(bytearray([REG_FIFO & 0x7F]))
    data = spi.read(n)
    CS.on()
    return data

# reset
RESET.value(0)
sleep(0.01)
RESET.value(1)
sleep(0.01)

print("Versão:", hex(spi_read_reg(0x42)))

# configurar freq 915
spi_write_reg(REG_FRF_MSB, 0xE4)
spi_write_reg(REG_FRF_MID, 0xC0)
spi_write_reg(REG_FRF_LSB, 0x00)

# config modem igual ao TX
spi_write_reg(0x1D, 0x72)
spi_write_reg(0x1E, 0x74)
spi_write_reg(0x26, 0x04)

# set FIFO RX base and ptr
spi_write_reg(REG_FIFO_RX_BASE, 0x00)
spi_write_reg(REG_FIFO_ADDR_PTR, 0x00)

# set RX continuous
spi_write_reg(REG_OP_MODE, 0x85)  # LONG_RANGE_MODE + MODE_RXCONTINUOUS

print("Servidor raw 915MHz ouvindo IRQ...")

while True:
    # opcional: mostra IRQ flags em loop pra depurar
    irq = spi_read_reg(REG_IRQ_FLAGS)
    #print("IRQ flags:", hex(irq))

    if DIO0.value() == 1:
        # le irq flags e limpa
        irq = spi_read_reg(REG_IRQ_FLAGS)
        print("IRQ flags:", hex(irq))
        # obter bytes recebidos
        nb = spi_read_reg(REG_RX_NB_BYTES)
        cur = spi_read_reg(REG_FIFO_RX_CURRENT_ADDR)
        # ajustar ponteiro
        spi_write_reg(REG_FIFO_ADDR_PTR, cur)
        if nb > 0:
            data = fifo_read(nb)
            print("RECV:", data)
        # limpar flags
        spi_write_reg(REG_IRQ_FLAGS, 0xFF)
    sleep(0.05)
