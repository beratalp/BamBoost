from spi import SPI
import time
import numpy


def spi_delay():
    time.sleep(15/1000)


def get_result(string):
    return string[2:6]


class BamBoostInclinometer:
    GETSTATUS = "180000E5"
    WHOAMI = "40000091"
    ENABLEANGLE = "B0001F6F1F"
    GETXANGLE = "240000C7"
    GETYANGLE = "280000CD"
    GETTEMPERATURE = "140000EF"

    def __init__(self, port = "/dev/spidev0.0"):
        self.spi = SPI(port)
        self.spi.mode = SPI.MODE_0
        self.spi.speed = 3000000
        spi_delay()
        self.__transfer__(BamBoostInclinometer.GETSTATUS)
        self.__transfer__(BamBoostInclinometer.GETSTATUS)
        self.__transfer__(BamBoostInclinometer.GETSTATUS)
        spi_delay()
        if not self.test_whoami():
            raise IOError("Sensor may not be plugged in.")
        self.__transfer__(BamBoostInclinometer.ENABLEANGLE)

    def __transfer__(self, string):
        if len(string) % 2 != 0:
            raise ValueError("Can't transfer odd number of hexadecimals")
        else:
            parts = [string[i:i + 2] for i in range(0, len(string), 2)]
            hexlist = []
            for part in parts:
                hexlist.append(int(part, 16))
            self.spi.write(hexlist)
            return str(self.spi.read(4).hex())

    def test_whoami(self):
        if get_result(self.__transfer__(BamBoostInclinometer.WHOAMI))[2:] == "c1":
            return True
        else:
            return False

    def getPitch(self):
        raw_angle = get_result(self.__transfer__(BamBoostInclinometer.GETXANGLE))
        raw_angle = numpy.int16(int(raw_angle, 16))
        return raw_angle / 2**14 * 90

    def getRoll(self):
        raw_angle = get_result(self.__transfer__(BamBoostInclinometer.GETYANGLE))
        raw_angle = numpy.int16(int(raw_angle, 16))
        return raw_angle / 2 ** 14 * 90

    def getTemperature(self):
        raw_temp = get_result(self.__transfer__(BamBoostInclinometer.GETTEMPERATURE))
        raw_temp = numpy.int16(int(raw_temp, 16))
        return str(round(-273 + raw_temp / 18.9, 2)) + " °C"

    def crc_test(self):
        while True:
            print("asdg")


