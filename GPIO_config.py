import RPi.GPIO as GPIO
import time

class io(object):


    def __init__(self, ):
        # SET GPIO numbering mode to use GPIO designation, NOT pin numbers
        GPIO.setmode(GPIO.BCM)

        """
        +--------------------+-----------+----+-----------+-------------------------+
        |                BCM | Header P1 | || | Header P1 | BCM                     |
        +--------------------+-----------+----+-----------+-------------------------+
        |         3.3V Power |         1 | || | 2         | 5V Power                |
        +--------------------+-----------+----+-----------+-------------------------+
        |        GPIO2 (SDA) |         3 | || | 4         | 5V Power                |
        +--------------------+-----------+----+-----------+-------------------------+
        |        GPIO3 (SCL) |         5 | || | 6         | GND                     |
        +--------------------+-----------+----+-----------+-------------------------+
        |     GPIO4 (GPCLK0) |         7 | || | 8         | GPIO14 (TXD0)           |
        +--------------------+-----------+----+-----------+-------------------------+
        |                GND |         9 | || | 10        | GPIO15 (RXD0)           |
        +--------------------+-----------+----+-----------+-------------------------+
        |  GPIO17 (SPI1 CE1) |        11 | || | 12        | GPIO18 (SPI1 CE0, PWM0) |
        +--------------------+-----------+----+-----------+-------------------------+
        |             GPIO27 |        13 | || | 14        | GND                     |
        +--------------------+-----------+----+-----------+-------------------------+
        |             GPIO22 |        15 | || | 16        | GPIO23                  |
        +--------------------+-----------+----+-----------+-------------------------+
        |               3.3V |        17 | || | 18        | GPIO24                  |
        +--------------------+-----------+----+-----------+-------------------------+
        | GPIO10 (SPI0 MOSI) |        19 | || | 20        | GND                     |
        +--------------------+-----------+----+-----------+-------------------------+
        |  GPIO9 (SPI0 MISO) |        21 | || | 22        | GPIO25                  |
        +--------------------+-----------+----+-----------+-------------------------+
        | GPIO11 (SPI0 SCLK) |        23 | || | 24        | GPIO8 (SPI0 CE0)        |
        +--------------------+-----------+----+-----------+-------------------------+
        |                GND |        25 | || | 26        | GPIO7 (SPI0 CE1)        |
        +--------------------+-----------+----+-----------+-------------------------+
        |      GPIO0 (ID_SD) |        27 | || | 28        | GPIO1 (ID_SC)           |
        +--------------------+-----------+----+-----------+-------------------------+
        |              GPIO5 |        29 | || | 30        | GND                     |
        +--------------------+-----------+----+-----------+-------------------------+
        |              GPIO6 |        31 | || | 32        | GPIO12 (PWM0)           |
        +--------------------+-----------+----+-----------+-------------------------+
        |      GPIO13 (PWM1) |        33 | || | 34        | GND                     |
        +--------------------+-----------+----+-----------+-------------------------+
        | GPIO19 (SPI1 MISO) |        35 | || | 36        | GPIO16                  |
        +--------------------+-----------+----+-----------+-------------------------+
        |             GPIO26 |        37 | || | 38        | GPIO20 (SPI1 MOSI)      |
        +--------------------+-----------+----+-----------+-------------------------+
        |                GND |        39 | || | 40        | GPIO21 (SPI1 SCLK)      |
        +--------------------+-----------+----+-----------+-------------------------+
        |                BCM | Header P1 | || | Header P1 | BCM                     |
        +--------------------+-----------+----+-----------+-------------------------+
     
        @dictionary GPIO Pin Numbers
        @Maps DAC singals to GPIO PINS.
        """
        self.pin_map = {
            "SDA_0": 2,
            "SCL_0": 3,
            "CLK_Bias": 4,
            "BCM5": 5,
            "BCM6": 6,
            "SPI0_CE1": 7,
            "SPI0_CE0": 8,
            "SPI0_MISO": 9,
            "SPI0_MOSI": 10,
            "SPI0_SCLK": 11,
            "BCM12": 12,
            "BCM13": 13,
            "BCM16": 16,
            "nADC_DRDY": 17,
            "nADC_RESET": 18,
            "BCM19": 19,
            "BCM20": 20,
            "BCM5": 21,
            "nADC_CS": 22,
            "nDAC_CS": 23,
            "Enable_28V_PS1": 24,
            "Enable_28V_PS2": 25,
            "BCM26": 26,
            "BCM27": 27,
        }

        # Set Enable_28V_PS1 to output.
        pin = self.pin_map['Enable_28V_PS1']
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 1)

        # Set Enable_28V_PS2 to output.
        pin = self.pin_map['Enable_28V_PS2']
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 1)

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

    def ps_28v_feed1_enable(self):
        pin = self.pin_map['Enable_28V_PS1']
        GPIO.output(pin, 0)

    def ps_28v_feed1_disable(self):
        pin = self.pin_map['Enable_28V_PS1']
        GPIO.output(pin, 1)

    def ps_28v_feed2_enable(self):
        pin = self.pin_map['Enable_28V_PS2']
        GPIO.output(pin, 0)

    def ps_28v_feed2_disable(self):
        pin = self.pin_map['Enable_28V_PS2']
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
