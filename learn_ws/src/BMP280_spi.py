import spidev
import time

class BMP280_SPI:
    def __init__(self, spi_channel=0):
        self.spi = spidev.SpiDev()
        self.spi.open(0, spi_channel) 
        self.spi.max_speed_hz = 1000000 
        self.spi.mode = 0b00  

        
        self.dig_T1 = 0
        self.dig_T2 = 0
        self.dig_T3 = 0
        self.dig_P1 = 0
        self.dig_P2 = 0
        self.dig_P3 = 0
        self.dig_P4 = 0
        self.dig_P5 = 0
        self.dig_P6 = 0
        self.dig_P7 = 0
        self.dig_P8 = 0
        self.dig_P9 = 0
        
        self.load_calibration()
        self.write_register(0xF4, 0x2F)  

    def read_register(self, reg, length=1):
        reg |= 0x80 
        return self.spi.xfer2([reg] + [0]*length)[1:]

    def write_register(self, reg, data):
        reg &= 0x7F 
        self.spi.xfer2([reg, data])

    def load_calibration(self):
       
        calib = self.read_register(0x88, 24)
        
        self.dig_T1 = calib[1] << 8 | calib[0]
        self.dig_T2 = calib[3] << 8 | calib[2]
        if self.dig_T2 > 32767: self.dig_T2 -= 65536
        self.dig_T3 = calib[5] << 8 | calib[4]
        if self.dig_T3 > 32767: self.dig_T3 -= 65536

        self.dig_P1 = calib[7] << 8 | calib[6]
        self.dig_P2 = calib[9] << 8 | calib[8]
        if self.dig_P2 > 32767: self.dig_P2 -= 65536
        self.dig_P3 = calib[11] << 8 | calib[10]
        if self.dig_P3 > 32767: self.dig_P3 -= 65536
        self.dig_P4 = calib[13] << 8 | calib[12]
        if self.dig_P4 > 32767: self.dig_P4 -= 65536
        self.dig_P5 = calib[15] << 8 | calib[14]
        if self.dig_P5 > 32767: self.dig_P5 -= 65536
        self.dig_P6 = calib[17] << 8 | calib[16]
        if self.dig_P6 > 32767: self.dig_P6 -= 65536
        self.dig_P7 = calib[19] << 8 | calib[18]
        if self.dig_P7 > 32767: self.dig_P7 -= 65536
        self.dig_P8 = calib[21] << 8 | calib[20]
        if self.dig_P8 > 32767: self.dig_P8 -= 65536
        self.dig_P9 = calib[23] << 8 | calib[22]
        if self.dig_P9 > 32767: self.dig_P9 -= 65536

    def read_raw_data(self):
        data = self.read_register(0xF7, 6)
        press_raw = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
        temp_raw = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
        return temp_raw, press_raw

    def compensate_temperature(self, temp_raw):
        var1 = ((temp_raw / 16384.0) - (self.dig_T1 / 1024.0)) * self.dig_T2
        var2 = (((temp_raw / 131072.0) - (self.dig_T1 / 8192.0)) * 
               ((temp_raw / 131072.0) - (self.dig_T1 / 8192.0))) * self.dig_T3
        t_fine = var1 + var2
        temperature = (var1 + var2) / 5120.0
        return temperature, t_fine

    def compensate_pressure(self, press_raw, t_fine):
        var1 = t_fine / 2.0 - 64000.0
        var2 = var1 * var1 * (self.dig_P6) / 32768.0
        var2 = var2 + var1 * (self.dig_P5) * 2.0
        var2 = var2 / 4.0 + (self.dig_P4) * 65536.0
        var1 = ((self.dig_P3) * var1 * var1 / 524288.0 + (self.dig_P2) * var1) / 524288.0
        var1 = (1.0 + var1 / 32768.0) * (self.dig_P1)
        if var1 == 0:
            return 0
        pressure = 1048576.0 - press_raw
        pressure = (pressure - (var2 / 4096.0)) * 6250.0 / var1
        var1 = (self.dig_P9) * pressure * pressure / 2147483648.0
        var2 = pressure * (self.dig_P8) / 32768.0
        pressure = pressure + (var1 + var2 + (self.dig_P7)) / 16.0
        return pressure / 100.0 

    def read_data(self):
        temp_raw, press_raw = self.read_raw_data()
        temperature, t_fine = self.compensate_temperature(temp_raw)
        pressure = self.compensate_pressure(press_raw, t_fine)
        return temperature, pressure


if __name__ == "__main__":
    sensor = BMP280_SPI(spi_channel=0)  
    
    try:
        while True:
            temperature, pressure = sensor.read_data()
            print(f"Temperature: {temperature:.2f} °C")
            print(f"Pressure: {pressure:.2f} hPa")
            print("-----------------------")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting...")
