import RPi.GPIO as GPIO
import time
import signal
import sys


IN1 = 12   
IN2 = 16   
EN = 21    


GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(EN, GPIO.OUT)


pwm = GPIO.PWM(EN, 1000)  
pwm.start(0)             

def motor_forward(speed=100):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    pwm.ChangeDutyCycle(speed)

def motor_backward(speed=100):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    pwm.ChangeDutyCycle(speed)

def motor_stop():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    pwm.ChangeDutyCycle(0)

def cleanup_and_exit(signum=None, frame=None):
    print("Cleaning up GPIO and exiting...")
    motor_stop()
    pwm.stop()
    GPIO.cleanup()
    sys.exit(0)

signal.signal(signal.SIGTERM, cleanup_and_exit)
signal.signal(signal.SIGINT, cleanup_and_exit)  

try:
    print("Motor forward for 3 seconds...")
    motor_forward(80)
    time.sleep(3)

    print("Motor backward for 3 seconds...")
    motor_backward(80)
    time.sleep(3)

    print("Stopping motor")
    motor_stop()

    cleanup_and_exit()  

except Exception as e:
    print(f"Error occurred: {e}")
    cleanup_and_exit()
