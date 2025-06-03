import time
import board
import busio
import signal
import sys
from adafruit_ssd1306 import SSD1306_I2C
from PIL import Image, ImageDraw, ImageFont


i2c = busio.I2C(board.SCL, board.SDA)


oled = SSD1306_I2C(128, 64, i2c, addr=0x3C)

def clear_display():
    oled.fill(0)
    oled.show()

def handle_exit(signum=None, frame=None):
    print("Cleaning up OLED...")
    clear_display()
    sys.exit(0)

signal.signal(signal.SIGTERM, handle_exit)
signal.signal(signal.SIGINT, handle_exit)

try:
 
    clear_display()

    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)

    
    font = ImageFont.load_default()

    
    draw.text((0, 0), "Hello, OLED!", font=font, fill=255)
    draw.text((0, 16), "Using I2C @ 0x3C", font=font, fill=255)
    draw.text((0, 32), "Raspberry Pi 4", font=font, fill=255)

    oled.image(image)
    oled.show()

    time.sleep(5)  

    handle_exit()

except Exception as e:
    print(f"Error: {e}")
    handle_exit()
