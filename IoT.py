import RPi.GPIO as rpi_gpio
from time import time, sleep

sensors_height = 200 #Tinggi sensor

class Sensors:
    def __init__(self, trigger:int = 4, echo:int = 17) -> None:
        self.trigger = trigger
        self.echo = echo
        self.gpio = rpi_gpio
        
        self.gpio.setmode(self.gpio.BCM)
        self.gpio.setwarnings(False)

        self.gpio.setup(self.trigger, self.gpio.OUT)
        self.gpio.setup(self.echo, self.gpio.IN)
        self.gpio.output(self.trigger, self.gpio.LOW)

    def __trigger__(self):
        self.gpio.output(self.trigger, True)
        sleep(0.00001)
        self.gpio.output(self.trigger, False)

    def __echo__(self):
        time_start = time()
        timeout = int(time())
        while(self.gpio.input(self.echo) != 1):
            time_start = time()
            if(int(time()) - timeout >= 6):
                return -1
        return ((time() - time_start) * 34320) / 2) * 100
    
    def get_data(self):
        self.__trigger__()
        result = self.__echo__()
        if(result == -1):
            print("Gagal mendapatkan data dari sensor")
        else:
            print(f"Tinggi badan : {sensors_height - result} Cm")

try:
    s = Sensors()
    while(True):
        s.get_data()
        sleep(1)
except:
    rpi_gpio.cleanup()
