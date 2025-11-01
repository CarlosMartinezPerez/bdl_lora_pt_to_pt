from ulora import LoRa, SPIConfig
from time import sleep

RFM95_RST = 28
RFM95_SPIBUS = SPIConfig.rp2_0
RFM95_CS = 17
RFM95_INT = 20
RF95_FREQ = 868.0

SERVER_ADDRESS = 2

def on_recv(payload):
    print("RECV:", payload.message)

lora = LoRa(RFM95_SPIBUS, RFM95_INT, SERVER_ADDRESS, RFM95_CS,
            reset_pin=RFM95_RST, freq=RF95_FREQ, tx_power=14, acks=True)

lora.on_recv = on_recv
lora.set_mode_rx()

print("SERVER pronto")

while True:
    sleep(0.1)
