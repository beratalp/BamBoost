from adxl345 import *
import math


class BamBoostInclinometer:
    def __init__(self):
        self.inclinometer = ADXL345()

    def getX(self):
        try:
            return self.inclinometer.get_axes()["x"]
        except:
            return self.getX()

    def getY(self):
        try:
            return self.inclinometer.get_axes()["y"]
        except:
            return self.getY()

    def getZ(self):
        try:
            return self.inclinometer.get_axes()["z"]
        except:
            return self.getZ()

    def getPitch(self):
        return math.degrees(math.atan2(self.getY(), math.sqrt(math.pow(self.getX(), 2) + math.pow(self.getZ(), 2))))

    def getRoll(self):
        return math.degrees(math.atan2(0 - self.getX(), self.getZ()))