from ulora import LoRa, SPIConfig
from time import sleep

RFM95_RST = 28
RFM95_SPIBUS = SPIConfig.rp2_0
RFM95_CS = 17
RFM95_INT = 20
RF95_FREQ = 868.0

CLIENT_ADDRESS = 1
SERVER_ADDRESS = 2

lora = LoRa(RFM95_SPIBUS, RFM95_INT, CLIENT_ADDRESS, RFM95_CS,
            reset_pin=RFM95_RST, freq=RF95_FREQ, tx_power=14, acks=True)

print("CLIENT pronto")

while True:
    lora.send_to_wait("TESTE", SERVER_ADDRESS)
    print("enviado: TESTE")
    sleep(2)
