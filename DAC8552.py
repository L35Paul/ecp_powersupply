import GPIO_config
import time


class DAC8552(object):

    def __init__(self, ecpdb, spi_obj):
        self.pins = GPIO_config.io()
        self._vref = 3.3
        self.db = ecpdb
        self._DUMMY_BYTE = 0xff
        self._READ_FLAG = 0b01000000
        self.spi_obj = spi_obj
        self.__dac_initialize()

    def __delete__(self, instance):
        self.spi_obj.close()

    def dac_set_output_voltage(self, channel, voltage):
        # read input_shift_register reg
        hexdata = self.__dac_voltage_convert(self._vref, voltage)
        hexdata &= 0xFFFF
        dict_isr = self.db.db_dac8552_fetch_names_n_values('input_shift_register')
        dict_isr['data']= hexdata
        dict_isr['buffer_select'] = channel
        dict_isr['LDA'] = 1
        dict_isr['LDB'] = 1
        self.__dac_write_register('input_shift_register', **dict_isr)

    def __dac_voltage_convert(self, Vref, voltage):

        _D_=0
        _D_ = (int)(65536 * voltage / Vref)
        return _D_

    def __dac_initialize(self):
        self.RegAddrs = self.db.db_table_data_to_dictionary('tblDac8552Registers')

    def __dac_write_register(self, reg_name, **kwargs):
        reg_dict = self.db.db_dac8552_register_data_to_dictionary(reg_name)
        write_bytes = self.__dac_getbytes_from_reg_bits(kwargs, reg_dict)

        rbytes = write_bytes.to_bytes((write_bytes.bit_length() + 7) // 8, byteorder='big')

        bytelist = []
        for val in rbytes:
            bytelist.append(val)

        self.pins.dac_enable()
        self.spi_obj.xfer2(bytelist)
        self.pins.dac_disable()

    def __search_reg_address_from_name(self, name):
        for a in self.RegAddrs:
            if a['NAME'] == name:
                return a['ADDRESS']
        return -1

    def __search_reg_bytes_from_name(self, name):
        for a in self.RegAddrs:
            if a['NAME'] == name:
                return a['BYTES']
        return -1

    def __dac_getbytes_from_reg_bits(self, kwargs, reg_dict):
        write_bytes = 0x0000
        for kword in kwargs:
            for item in reg_dict:
                if item["NAME"] == kword:
                    name = item["NAME"]
                    value = int(kwargs[name])
                    shift = item["SHIFT"]
                    mask = item["MASK"]
                    write_bytes = write_bytes | ((value & mask) << shift)
        return write_bytes







