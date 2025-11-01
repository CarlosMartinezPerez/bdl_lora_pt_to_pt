# Comunicação LoRa entre duas placas BitDogLab

Estrutura geral do projeto

O projeto implementa comunicação LoRa ponto a ponto (não LoRaWAN), usando a biblioteca ulora.py — uma implementação em MicroPython para o rádio Semtech SX1276/77/78/79, que é o chip interno do RFM95W.

Os módulos principais são:

| Arquivo      | Função principal                                                                                               |
|---------------|---------------------------------------------------------------------------------------------------------------|
| ulora.py    | Driver LoRa completo, com configuração SPI, controle de modos (TX, RX, CAD), ACKs e interrupções via GPIO.     |
| client.py   | Protótipo simples de cliente LoRa (envia mensagem fixa).                                                       |
| client2.py  | Versão interativa do cliente (envia mensagem ao pressionar botão).                                             |
| server.py   | Servidor que recebe mensagens e mostra no display OLED.                                                        |
| server2.py  | Versão do servidor que também responde ao código ‘5’, alternando o LED vermelho.                               |
| pinagem.txt | Tabela de conexão entre o módulo RFM95W e o Pico (BitDogLab v7).                                               |


Interpretação da resposta do módulo RFM95W ao registrador de versão (0x42):


|Resultado|Significado|
|---------|-----------|
|0x12|	rádio OK e reconhecido|
|0x00 ou 0xFF|	rádio não respondendo (pinos errados / sem alimentação / CS errado)|
|travou|	bug nos pinos SPI (não está liberando CS ou SPI errado)|