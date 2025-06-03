import time
import busio
import digitalio
import board
from adafruit_mcp3xxx.mcp3008 import MCP3008
from adafruit_mcp3xxx.analog_in import AnalogIn
from adafruit_mcp3xxx.mcp3008 import P0, P1, P2, P3, P4, P5, P6, P7  


spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.CE1)  

mcp = MCP3008(spi, cs)

channels = [
    AnalogIn(mcp, P0),
    AnalogIn(mcp, P1),
    AnalogIn(mcp, P2),
    AnalogIn(mcp, P3),
    AnalogIn(mcp, P4),
    AnalogIn(mcp, P5),
    AnalogIn(mcp, P6),
    AnalogIn(mcp, P7),
]


while True:
    for i, chan in enumerate(channels):
        print(f"Channel {i}: Raw = {chan.value}, Voltage = {chan.voltage:.2f} V")
    print("-" * 40)
    time.sleep(0.5)
