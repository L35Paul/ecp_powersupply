#!/usr/bin/env python3
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from EcpGuiWindow import MainWindow
import DAC8552
import ADS1256
from db import ecp_db
import GPIO_config
import spidev
import RPi.GPIO as GPIO

def main():

    db = ecp_db()
    # create IO object
    io = GPIO_config.io()
    # Create SPI Bus object
    spi = spidev.SpiDev()  # create spi object
    spi_id = 0
    cs_id = 0
    spi.open(spi_id, cs_id)
    spi.max_speed_hz = 7000
    spi.mode = 1
    # spi.lsbfirst = False
    # spi.no_cs = False
    dac8552 = DAC8552.DAC8552(db,spi)
    adc1256 = ADS1256.ADS1256(db,spi)

    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow(db, dac8552, adc1256)
    main_window.show()
    app.exec_()

    GPIO.cleanup()


if __name__ == "__main__":
    main()
