import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSql import *


class ecp_db(object):

    def __init__(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("ecp.db")

        if not self.db.open():
            result = QMessageBox.warning(None, 'Phone Log', "Database Error: %s" % self.db.lastError().text())
            print(result)
            sys.exit(1)

    def db_fetch_table_fields(self, tblname):
        query = QSqlQuery(self.db)
        qrytxt = "pragma table_info({tn})".format(tn=tblname)
        query.exec_(qrytxt)
        tblheader = []
        while query.next():
            tblheader.append(query.value(1))
        return tblheader

    def db_fetch_table_data(self, tblname):
        query = QSqlQuery(self.db)
        query.exec_("SELECT * FROM " + tblname)
        data_list = []
        while query.next():
            i = 0
            data = {}
            while query.value(i) is not None:
                data[i] = query.value(i)
                i += 1
            data_list.append(data)
        return data_list

    def db_table_data_to_dictionary(self, tblname):
        query = QSqlQuery(self.db)
        query.exec_("SELECT * FROM " + tblname)
        data_list = []
        column_names = self.db_fetch_table_fields(tblname)
        data_dict = {}
        i = 0
        while query.next():
            for i in range(len(column_names)):
                data_dict[column_names[i]] = query.value(i)
                data_list.append(data_dict)
            data_dict = {}

        return data_list

    def db_fetch_tablenames(self):
        query = QSqlQuery(self.db)
        qrytxt = ("SELECT name FROM sqlite_master "
                  "WHERE type IN ('table','view') AND name NOT LIKE 'sqlite_%' "
                  "UNION ALL "
                  "SELECT name FROM sqlite_temp_master "
                  "WHERE type IN ('table','view') ORDER BY 1")
        query.exec_(qrytxt)
        print(qrytxt)
        list = []
        while query.next():
            list.append(query.value(0))
        return list

    def db_fetch_adc1256_command(self, cmd_name):
        tablename = 'tblAdc1256Commands'
        query = QSqlQuery(self.db)

        qrytxt = "select {command}, {first}, {second} from {tn} where COMMAND = '{cn}'" \
            .format(command="COMMAND", first="FIRSTBYTE",
                    second= "SECONDBYTE", tn = tablename, cn=cmd_name)
        data_dict = {}
        data = []
        query.exec_(qrytxt)
        while query.next():
            data_dict["COMMAND"] = query.value(0)
            data_dict["FIRSTBYTE"] = query.value(1)
            data_dict["SECONDBYTE"] = query.value(2)
            data.append(data_dict)
            data_dict = {}
        return data

    def db_adc1256_fetch_names_n_values(self, regname):
        # Retrive sub register names and values for a given register.
        query = QSqlQuery(self.db)
        tablename = 'tblAdc1256RegBits'

        qrytxt = "select {name}, {value} from {tn} inner join tblAdc1256Registers on {parent} = tblAdc1256Registers.ADDRESS " \
                 "where tblAdc1256Registers.NAME = '{rn}'".format(name=tablename + ".NAME",
                                                              value=tablename + ".VALUE",
                                                              tn=tablename, parent=tablename + ".FK_PARENT_ID",
                                                              rn=regname)
        query.exec_(qrytxt)
        regdict = {}

        while query.next():
            regdict[query.value(0)] = query.value(1)

        return regdict

    def db_adc_register_data_to_dictionary(self, regname):
        tablename = 'tblAdc1256RegBits'
        query = QSqlQuery(self.db)

        qrytxt = "select {name}, {mask}, {shift}, {value} ,{parent} from {tn} inner join tblAdc1256Registers on " \
                 "{parent} = tblAdc1256Registers.ADDRESS where tblAdc1256Registers.NAME = '{rn}'" \
            .format(name=tablename + ".NAME", mask=tablename + ".MASK", shift=tablename + ".SHIFT",
                    value=tablename + ".VALUE", parent=tablename + ".FK_PARENT_ID", tn=tablename, rn=regname)
        data_dict = {}
        data = []
        query.exec_(qrytxt)

        while query.next():
            data_dict["NAME"] = query.value(0)
            data_dict["MASK"] = query.value(1)
            data_dict["SHIFT"] = query.value(2)
            data_dict["VALUE"] = query.value(3)
            data_dict["PK_PAPRENT_ID"] = query.value(4)

            data.append(data_dict)
            data_dict = {}
        return data


    # <editor-fold desc="*************** dac8552 Queries ******************">

    def db_dac8552_register_data_to_dictionary(self, regname):
        tablename = 'tbldac8552RegBits'
        query = QSqlQuery(self.db)

        qrytxt = "select {name}, {mask}, {shift}, {value} ,{parent} from {tn} inner join tbldac8552Registers on " \
                 "{parent} = tbldac8552Registers.ADDRESS where tbldac8552Registers.NAME = '{rn}'" \
            .format(name=tablename + ".NAME", mask=tablename + ".MASK", shift=tablename + ".SHIFT",
                    value=tablename + ".VALUE", parent=tablename + ".FK_PARENT_ID", tn=tablename, rn=regname)
        data_dict = {}
        data = []
        query.exec_(qrytxt)

        while query.next():
            data_dict["NAME"] = query.value(0)
            data_dict["MASK"] = query.value(1)
            data_dict["SHIFT"] = query.value(2)
            data_dict["VALUE"] = query.value(3)
            data_dict["PK_PAPRENT_ID"] = query.value(4)

            data.append(data_dict)
            data_dict = {}
        return data

    def db_dac8552_fetch_names_n_values(self, regname):

        query = QSqlQuery(self.db)
        tablename = 'tbldac8552RegBits'

        qrytxt = "select {name}, {value} from {tn} inner join tbldac8552Registers on {parent} = tbldac8552Registers.ADDRESS " \
                 "where tbldac8552Registers.NAME = '{rn}'".format(name=tablename + ".NAME",
                                                              value=tablename + ".VALUE",
                                                              tn=tablename, parent=tablename + ".FK_PARENT_ID",
                                                              rn=regname)
        query.exec_(qrytxt)
        regdict = {}

        while query.next():
            regdict[query.value(0)] = query.value(1)

        return regdict

    # </editor-fold>

    def __del__(self):
        self.db.close()


class DbTableModel(QAbstractTableModel):


    def __init__(self, datain, headerdata, parent=None):
        """
        Args:
            datain: a list of lists\n
            headerdata: a list of strings
        """
        QAbstractTableModel.__init__(self, parent)
        self.arraydata = datain
        self.headerdata = headerdata

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        if len(self.arraydata) > 0:
            return len(self.arraydata[0])
        return 0

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
        return str(self.arraydata[index.row()][index.column()])

    def setData(self, index, value, role):
        pass         # not sure what to put here

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return str(self.headerdata[col])
        return None

    def sort(self, Ncol, order):
        """
        Sort table by given column number.
        """
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.arraydata = sorted(self.arraydata, key=operator.itemgetter(Ncol))
        if order == Qt.DescendingOrder:
            self.arraydata.reverse()
        self.emit(SIGNAL("layoutChanged()"))


def config_table(tv, tblheader, tabledata):
    # set the table model
    tablemodel = DbTableModel(tabledata, tblheader)
    tv.setModel(tablemodel)
    # set the minimum size
    tv.setMinimumSize(400, 300)
    # hide grid
    tv.setShowGrid(True)
    # hide vertical header
    vh = tv.verticalHeader()
    vh.setVisible(False)
    # set horizontal header properties
    hh = tv.horizontalHeader()
    hh.setStretchLastSection(True)
    # set column width to fit contents
    tv.resizeColumnsToContents()
    # set row height
    tv.resizeRowsToContents()
    # enable sorting
    tv.setSortingEnabled(False)
