import busio
import digitalio
import board
import time

from adafruit_mcp3xxx.mcp3008 import MCP3008, P0
from adafruit_mcp3xxx.analog_in import AnalogIn


spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)


cs = digitalio.DigitalInOut(board.CE1)

mcp = MCP3008(spi, cs)


chan0 = AnalogIn(mcp, P0)

while True:
    print(f"Raw ADC Value: {chan0.value}, Voltage: {chan0.voltage:.2f} V")
    time.sleep(0.5)
