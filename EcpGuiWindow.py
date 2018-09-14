from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
import ecp_ps_gui
import re


class MainWindow(QtWidgets.QMainWindow,  ecp_ps_gui.Ui_MainWindow):


    def __init__(self, db, dac8552, ads1256):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.db = db
        self.dac8552 = dac8552
        self.ads1256 = ads1256
        self.__gui_delegates()
        self._vref = 2.5
        self._pga = 1

        tblnames = self.db.db_fetch_tablenames()
        adc_registers = self.db.db_fetch_table_data('tblAdc1256Registers')
        for adc_register in adc_registers:
            self.cboAdcRegisters.addItem(adc_register[0])
        self.cboAdcRegisters.setCurrentIndex(1)


    def __gui_delegates(self):
        self.btnSetDacOut1.released.connect(self.__set_dac1_volts)
        self.btnSetDacOut2.released.connect(self.__set_dac2_volts)
        self.btnReadAdcRegister.released.connect(self.__adc_read_register)
        self.btnReadAdcs.released.connect(self.__read_adcs)

    def __read_adcs(self):
        for checkbox in self.grpAdcs.findChildren(QtWidgets.QCheckBox):
            if checkbox.isChecked() is True:
                name = checkbox.text()
                chbxid = int(re.search(r'\d+', name).group())
                counts = self.ads1256.read_adc_conversion(chbxid - 1)
                volts = counts * (2 * self._vref/(self._pga * ((2**23) - 1)))
        self.txtDisplay.append('Counts = {0:d} volts = {1:.3f}'.format(counts,volts))

    def __set_dac1_volts(self):
        voltage = self.spinDacOut1.value()
        self.dac8552.dac_set_output_voltage(0, voltage)

    def __set_dac2_volts(self):
        voltage = self.spinDacOut2.value()
        self.dac8552.dac_set_output_voltage(1, voltage)

    def __adc_read_register(self):
        self.txtDisplay.clear()
        tablename = self.cboAdcRegisters.currentText()
        status = self.ads1256.adc_read_register_to_dict(tablename)
        for key, value in sorted(status.items()):
            self.txtDisplay.append(key + " " + str(value))
