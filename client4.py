from machine import Pin, SoftI2C
from time import sleep
from ulora import LoRa, SPIConfig
from ssd1306 import SSD1306_I2C

# ===== OLED =====
i2c = SoftI2C(scl=Pin(3), sda=Pin(2))
oled = SSD1306_I2C(128, 64, i2c)

# ===== LEDS =====
verde = Pin(11, Pin.OUT)
azul = Pin(12, Pin.OUT)
vermelho = Pin(13, Pin.OUT)

# ===== Botão =====
botao_a = Pin(5, Pin.IN, Pin.PULL_UP)

# ===== LoRa =====
RFM95_RST = 28
RFM95_SPIBUS = SPIConfig.rp2_0
RFM95_CS = 17
RFM95_INT = 20
RF95_FREQ = 868.0
RF95_POW = 10
CLIENT_ADDRESS = 1
SERVER_ADDRESS = 2

lora = LoRa(RFM95_SPIBUS, RFM95_INT, CLIENT_ADDRESS, RFM95_CS,
            reset_pin=RFM95_RST, freq=RF95_FREQ, tx_power=RF95_POW, acks=True)

azul.on()

# mensagem no display ao iniciar
oled.fill(0)
oled.text("CLIENTE LORA", 10, 15)
oled.text("Pronto...", 25, 35)
oled.show()

def enviar(texto):
    print("Enviando:", texto)
    lora.send_to_wait(texto, SERVER_ADDRESS)

    # pisca LED vermelho 3 vezes
    for _ in range(3):
        vermelho.on()
        sleep(0.12)
        vermelho.off()
        sleep(0.12)

    # escreve no OLED após envio
    oled.fill(0)
    oled.text("Cliente enviou:", 0, 10)
    oled.text(texto, 0, 25)
    oled.show()

# ===== loop =====
while True:
    if botao_a.value() == 0:   # pressionado
        enviar("5")
        sleep(0.3)  # debouncing
