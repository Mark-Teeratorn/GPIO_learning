import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)


relay_pins = [20, 13, 4, 25]  


for pin in relay_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)  

try:
    while True:
        for i, pin in enumerate(relay_pins):
            print(f"Turning ON Relay {i+1}")
            GPIO.output(pin, GPIO.LOW)  
            time.sleep(1)

            print(f"Turning OFF Relay {i+1}")
            GPIO.output(pin, GPIO.HIGH)  
            time.sleep(1)

except KeyboardInterrupt:
    print("Exiting program...")

finally:
    
    GPIO.cleanup()
