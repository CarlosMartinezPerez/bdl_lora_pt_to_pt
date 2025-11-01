from machine import Pin, SoftI2C
from ssd1306 import SSD1306_I2C
from time import sleep

# configuração do display
i2c = SoftI2C(scl=Pin(15), sda=Pin(14))
oled = SSD1306_I2C(128, 64, i2c)

# teste
oled.fill(0) # limpa
oled.text("OLED OK!", 10, 10)
oled.text("BitDogLab v6", 10, 30)
oled.show()

print("Finalizado.")
