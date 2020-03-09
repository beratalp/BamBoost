import RPi.GPIO as GPIO
import time
import math


class LinearMotor:
    def __init__(self, pin1, pin2):
        self.pin1 = pin1
        self.pin2 = pin2
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin1, GPIO.OUT)
        GPIO.setup(self.pin2, GPIO.OUT)
        GPIO.output(self.pin1, 0)
        GPIO.output(self.pin2, 0)

    def __reset__(self):
        GPIO.output(self.pin1, 0)
        GPIO.output(self.pin2, 0)

    def negative(self, duration, speed):
        self.__reset__()
        speed = round(speed, 2)
        pwm = GPIO.PWM(self.pin1, 2000)
        pwm.start(speed)
        time.sleep(duration)
        pwm.stop()
        self.__reset__()

    def positive(self, duration, speed):
        self.__reset__()
        speed = round(speed, 2)
        pwm = GPIO.PWM(self.pin2, 2000)
        pwm.start(speed)
        time.sleep(duration)
        pwm.stop()
        self.__reset__()