import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
p = GPIO.PWM(11, 50)
p.start(12.5)
count = 0
try:
    while count <= 3:
        p.ChangeDutyCycle(12.5)
        time.sleep(1)
        p.ChangeDutyCycle(2.5)
        time.sleep(1)
        count += 1
except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()
