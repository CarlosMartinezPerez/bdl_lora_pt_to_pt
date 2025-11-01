from machine import Pin
from time import sleep

# Define os pinos dos LEDs RGB
led_vermelho = Pin(13, Pin.OUT)
led_verde = Pin(11, Pin.OUT)
led_azul = Pin(12, Pin.OUT)

while True:
    led_vermelho.on()
    sleep(0.2)
    led_vermelho.off()

    led_verde.on()
    sleep(0.2)
    led_verde.off()

    led_azul.on()
    sleep(0.2)
    led_azul.off()
