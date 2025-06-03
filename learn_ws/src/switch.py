import subprocess
import time
import RPi.GPIO as GPIO


BUTTON_PIN = 14
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

scripts = [
    "relay.py",
    "BH1750.py",
    "BMP280_spi.py",
    "hc-sr04.py",
    "L293B.py",
    "oled_display.py",
    "read_MCP3008.py",
    "stepper_motor.py"
]

press_count = 0
index = 0  
script_running = False  
process = None  

def button_pressed(channel):
    global press_count
    press_count += 1
    print(f"Button pressed! Count: {press_count}")

GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_pressed, bouncetime=300)

try:
    while True:
        if press_count > 0:
            if not script_running: 
                print(f"Starting script {scripts[index]}...")
                process = subprocess.Popen(["python3", scripts[index]])
                script_running = True
            else:  
                print(f"Stopping script {scripts[index]}...")
                if process:
                    process.terminate()
                    process = None
                script_running = False
                index = (index + 1) % len(scripts)  
            
            press_count = 0  
            time.sleep(0.5)  
except KeyboardInterrupt:
    print("Cycle stopped by user.")
    if process:
        process.terminate()  
finally:
    GPIO.cleanup()  

