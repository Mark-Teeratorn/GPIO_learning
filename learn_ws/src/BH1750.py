import smbus2
import time

BH1750_ADDRESS = 0x23
bus = smbus2.SMBus(1)
CONTINUOUS_HIGH_RES_MODE = 0x10

def read_light():
    bus.write_byte(BH1750_ADDRESS, CONTINUOUS_HIGH_RES_MODE)
    time.sleep(0.18)

    data = bus.read_i2c_block_data(BH1750_ADDRESS, 0x00, 2)
    raw_lux = (data[0] << 8) | data[1]
    lux = raw_lux/1.2
    return lux

try:
    while True:
        lux = read_light()
        print(f"Light level: {lux:.2f} lux")
        time.sleep(1)

except KeyboardInterrupt:
    print("Stopped")
