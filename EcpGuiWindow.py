from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
import ecp_ps_gui
import re
import GPIO_config
from db import config_table

class MainWindow(QtWidgets.QMainWindow,  ecp_ps_gui.Ui_MainWindow):


    def __init__(self, db, dac8552, ads1256):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.db = db
        self.pins = GPIO_config.io()
        self.dac8552 = dac8552
        self.ads1256 = ads1256
        self.__gui_delegates()
        self._vref = 2.5
        self.tabMain.setCurrentIndex(0)

        adc_registers = self.db.db_fetch_table_data('tblAdc1256Registers')
        for adc_register in adc_registers:
            self.cboAdcRegisters.addItem(adc_register[0])
        self.cboAdcRegisters.setCurrentIndex(1)
        tblnames = self.db.db_fetch_tablenames()
        for i in range(len(tblnames)):
            line = re.sub('[!@#$,()\']', '', str(tblnames[i]))
            self.cboDatabaseTableNames.addItem(line)

    def __gui_delegates(self):
        self.btnSetDacOut1.released.connect(self.__set_dac1_volts)
        self.btnSetDacOut2.released.connect(self.__set_dac2_volts)
        self.btnReadAdcRegister.released.connect(self.__adc_read_register)
        self.btnReadAdcs.released.connect(self.__read_adcs)
        self.btnStoreAdcChanConfig.released.connect(self.__config_ad_channel)
        self.cboDatabaseTableNames.currentIndexChanged.connect(self.__read_tabledata_from_db)
        self.btnSetPsVoltage.released.connect(self.__set_ps_voltage)
        self.radPSIn1Sel.released.connect(self.__toggle_ps1)
        self.radPSIn2Sel.released.connect(self.__toggle_ps2)

    def __toggle_ps1(self):
        state = self.radPSIn1Sel.isChecked()
        if state is True:
            self.pins.ps_28v_feed1_enable()
        else:
            self.pins.ps_28v_feed1_disable()

    def __toggle_ps2(self):
        state = self.radPSIn2Sel.isChecked()
        if state is True:
            self.pins.ps_28v_feed2_enable()
        else:
            self.pins.ps_28v_feed2_disable()

    def __set_ps_voltage(self):
        voltage = self.spinPsVoltage.value()
        setval = (-0.1239 * voltage) + 4.9644
        self.dac8552.dac_set_output_voltage(0, setval)


    def __read_tabledata_from_db(self):
        tblname = self.cboDatabaseTableNames.currentText()
        tabledata = self.db.db_fetch_table_data(tblname)
        tblheader = self.db.db_fetch_table_fields(tblname)
        self.table = config_table(self.tableView, tblheader, tabledata)


    def __config_ad_channel(self):
        chan_dict={}
        chan_dict['chid'] = self.spinSelAdcChan.value()
        chan_dict['nsel'] = self.cboNegSel.currentIndex()
        chan_dict['psel'] = self.cboPosSel.currentIndex()
        gainidx = self.cboAdcChGain.currentIndex()
        chan_dict['gain'] = 2**gainidx
        self.db.store_ads1256_channel_config(**chan_dict)

    def __read_adcs(self):
        self.txtDisplay.clear()
        for checkbox in self.grpAdcs.findChildren(QtWidgets.QCheckBox):
            if checkbox.isChecked() is True:
                name = checkbox.text()
                chbxid = int(re.search(r'\d+', name).group())
                counts = self.ads1256.read_adc_conversion(chbxid - 1)
                volts = counts * (2 * self._vref/((2**23) - 1))
                self.txtDisplay.append('Counts{0:d} = {1:d} volts = {2:.3f}'.format(chbxid,counts,volts))

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
