from machine import Pin, SoftI2C

# configure I2C nos pinos do seu display
i2c = SoftI2C(sda=Pin(14), scl=Pin(15))

print("Procurando dispositivos I2C...")

devices = i2c.scan()

if len(devices) == 0:
    print("Nenhum dispositivo I2C encontrado :(")
else:
    print("Dispositivos encontrados:")
    for d in devices:
        print("I2C address:", hex(d))
