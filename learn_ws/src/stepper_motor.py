import RPi.GPIO as GPIO
import time


IN1 = 17  
IN2 = 18  
IN3 = 27  
IN4 = 22  


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


for pin in [IN1, IN2, IN3, IN4]:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)


halfstep_seq = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1]
]

def move_motor(steps, delay=0.001):
    for _ in range(steps):
        for halfstep in halfstep_seq:
            for pin, val in zip([IN1, IN2, IN3, IN4], halfstep):
                GPIO.output(pin, val)
            time.sleep(delay)

try:
    print("Rotating forward 512 steps (~360 degrees)...")
    move_motor(512)

    time.sleep(1)

    print("Rotating backward 512 steps...")
    move_motor(512, delay=0.001)
    halfstep_seq.reverse()  
    move_motor(512)
    halfstep_seq.reverse()  

finally:
    print("Cleaning up GPIO...")
    GPIO.cleanup()

