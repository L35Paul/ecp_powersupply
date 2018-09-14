import RPi.GPIO as GPIO
import time

class io(object):


    def __init__(self, ):
        """ SET GPIO numbering mode to use GPIO designation, NOT pin numbers """
        GPIO.setmode(GPIO.BCM)

        """
        @dictionary GPIO Pin Numbers
        @Maps DAC singals to GPIO PINS.
        """
        self.pin_map = {
            "SDA_0": 2,
            "SCL_0": 3,
            "GPCLK0": 4,
            "BCM5": 5,
            "BCM6": 6,
            "SPI0_CE1": 7,
            "SPI0_CE0": 8,
            "SPI0_MISO": 9,
            "SPI0_MOSI": 10,
            "SPI0_SCLK": 11,
            "BSM12": 12,
            "BSM13": 13,
            "BSM16": 16,
            "nADC_DRDY": 17,
            "nADC_RESET": 18,
            "BSM19": 19,
            "BSM20": 20,
            "spare5": 21,
            "nADC_CS": 22,
            "nDAC_CS": 23,
            "BSM24": 24,
            "BSM25": 25,
            "BSM26": 26,
            "BSM27": 27,
        }

        # Set /ADC_DRDY to output.
        pin = self.pin_map['nADC_DRDY']
        GPIO.setup(pin, GPIO.IN)

        # Set /ADC_RESET to input.
        pin = self.pin_map['nADC_RESET']
        GPIO.setup(pin, GPIO.OUT )
        GPIO.output(pin, 1)

        # Set /ADC_CS to output.
        pin = self.pin_map['nADC_CS']
        GPIO.setup(pin, GPIO.OUT )
        GPIO.output(pin, 1)

        # Set /DAC_CS to output.
        pin = self.pin_map['nDAC_CS']
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 1)


    def dac_enable(self):
        pin = self.pin_map['nDAC_CS']
        GPIO.output(pin, 1)
        GPIO.output(pin, 0)

    def dac_disable(self):
        pin = self.pin_map['nDAC_CS']
        GPIO.output(pin, 1)

    def adc_enable(self):
        pin = self.pin_map['nADC_CS']
        GPIO.output(pin, 1)
        GPIO.output(pin, 0)

    def adc_disable(self):
        pin = self.pin_map['nADC_CS']
        GPIO.output(pin, 1)

    def adc_ready(self):
        pin = self.pin_map['nADC_DRDY']
        if GPIO.input(pin) == 0:
            return True
        else:
            return False

    def adc_reset(self):
        pin = self.pin_map['nADC_RESET']
        GPIO.output(pin, 0)
        time.sleep(.001)
        GPIO.output(pin, 1)

