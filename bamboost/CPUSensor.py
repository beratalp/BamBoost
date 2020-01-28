import subprocess
import re


class CPUSensor:
    def __init__(self):
        self.command = "vcgencmd measure_temp"

    def getTemperature(self):
        temp_output = subprocess.check_output(self.command, shell=True)
        rr = re.findall(r"[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", temp_output.decode())
        return rr[0] + " °C"