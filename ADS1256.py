import time
import GPIO_config
import math

class ADS1256(object):
  

    def __init__(self, ecpdb, spi_obj):
        self._DUMMY_BYTE = 0x00
        self.pins = GPIO_config.io()
        self.db = ecpdb
        self.RegAddrs = []
        self.spi_obj = spi_obj
        self.__adc_initialize()

    def __delete__(self, instance):
        self.spi_obj.close()

    def read_adc_conversion(self, mux_chan):
        ch_dict = self.db.fetch_ads1256_channel_config(mux_chan)
        vals = ch_dict[0]
        self.__adc_write_input_mux(vals['PSEL_IN'], vals['NSEL_IN'])
        self.__adc_set_gain(vals['GAIN'])
        params = self.db.db_fetch_adc1256_command('RDATA')
        dictp = params[0]
        byte_list = [dictp['FIRSTBYTE'],self._DUMMY_BYTE,self._DUMMY_BYTE,self._DUMMY_BYTE]
        self.pins.adc_enable()
        data_24 = self.spi_obj.xfer2(byte_list)
        self.pins.adc_disable()
        data_24.pop(0)
        counts = (data_24[2] & 0x0000ff) + (data_24[1] << 8 & 0x00FF00) + (data_24[0] << 16 & 0xff0000)
        return (int)(counts/vals['GAIN'])

    def __adc_set_gain(self, gain):
        gainidx = math.log(gain,2)
        reg_name = 'ad_control'
        reg_dict = self.db.db_adc1256_fetch_names_n_values(reg_name)
        reg_dict["pga"] = gainidx
        self.__adc_write_register(reg_name, **reg_dict)
        result_dict = self.adc_read_register_to_dict(reg_name)
        if result_dict != reg_dict:
            raise ValueError

    """
    *	name: ads1256_readchipid
    *	function: Read the chip ID
    *	parameter: _cmd : NULL
    *	The return value: four high status register
    """
    def ads1256_readchipid(self):

        self.ads1256_wait_drdy()
        adcdict = self.adc_read_register_to_dict('status')
        return adcdict['id']

    """
    *	name: ads1256_wait_drdy
    *	function: delay time  wait for automatic calibration
    *	parameter:  NULL
    *	The return value:  NULL
    """
    def ads1256_wait_drdy(self):
        startticks = time.time()
        ready = False
        timeout = False
        while not ready and not timeout:
            ready = self.pins.adc_ready()
            if time.time() - startticks > 1000:
                timeout = True
        if timeout is True:
            print("Timeout Detected")

    def __adc_initialize(self):
        self.pins.adc_reset()
        self.RegAddrs = self.db.db_table_data_to_dictionary('tblAdc1256Registers')
        chipid = self.ads1256_readchipid()
        self.__configure_status_reg()
        print(chipid)

    def __configure_status_reg(self):
        reg_name = 'status'
        reg_dict = self.db.db_adc1256_fetch_names_n_values(reg_name)
        self.__adc_write_register(reg_name, **reg_dict)
        result_dict = self.adc_read_register_to_dict(reg_name)
        # if result_dict != reg_dict:
        #     raise ValueError

    def adc_read_register_to_dict(self, reg_name):
        reg_bit_data = self.db.db_adc_register_data_to_dictionary(reg_name)
        data_24 = self.__adc_read_register(reg_name)
        data_24.pop(0)
        value = int.from_bytes(data_24, byteorder='big', signed=False)
        dict_reg = dict()
        for item in reg_bit_data:
            keyname = item['NAME']
            dataval = (value >> item['SHIFT']) & item['MASK']
            dict_reg[keyname] = dataval
        return dict_reg

    def __adc_read_register(self, reg_name):
        params = self.db.db_fetch_adc1256_command('RREG')
        dictp = params[0]
        cmd = dictp['FIRSTBYTE']
        address = self.__search_reg_address_from_name(reg_name)
        command_byte1 = cmd << 4 | address
        command_byte2 = 0
        byte_list = [command_byte1,command_byte2, self._DUMMY_BYTE]
        self.pins.adc_enable()
        resp = self.spi_obj.xfer2(byte_list)
        self.pins.adc_disable()
        return resp

    def __adc_write_input_mux(self,psel,nsel):
        reg_name = 'input_mux_control'
        reg_dict = self.db.db_adc1256_fetch_names_n_values(reg_name)
        reg_dict["nsel"] = nsel
        reg_dict["psel"] = psel
        self.__adc_write_register(reg_name, **reg_dict)
        result_dict = self.adc_read_register_to_dict(reg_name)
        if result_dict != reg_dict:
            raise ValueError

    def __adc_write_register(self, reg_name, **kwargs):
        params = self.db.db_fetch_adc1256_command('WREG')
        dictp = params[0]
        cmd = dictp['FIRSTBYTE']
        command_byte2 = 0
        address = self.__search_reg_address_from_name(reg_name)
        command_byte1 = cmd << 4 | address
        reg_dict = self.db.db_adc_register_data_to_dictionary(reg_name)
        write_bytes = self.__adc1256_getbytes_from_reg_bits(kwargs, reg_dict)
        rbytes = write_bytes.to_bytes((write_bytes.bit_length() + 7) // 8, byteorder='big')

        bytelist = [command_byte1,command_byte2]
        for val in rbytes:
            bytelist.append(val)

        self.pins.adc_enable()
        self.spi_obj.xfer2(bytelist)
        self.pins.adc_disable()

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

    def __adc1256_getbytes_from_reg_bits(self, kwargs, reg_dict):
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