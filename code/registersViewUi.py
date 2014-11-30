# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uiRegistersView.ui'
#
# Created: Sun Nov 30 17:26:45 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_RegistersView(object):
    def setupUi(self, RegistersView):
        RegistersView.setObjectName("RegistersView")
        RegistersView.resize(641, 599)
        self.RegistersTable = QtGui.QTableWidget(RegistersView)
        self.RegistersTable.setGeometry(QtCore.QRect(0, 60, 421, 391))
        self.RegistersTable.setObjectName("RegistersTable")
        self.RegistersTable.setColumnCount(4)
        self.RegistersTable.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.RegistersTable.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.RegistersTable.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.RegistersTable.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.RegistersTable.setHorizontalHeaderItem(3, item)
        self.FormulasTable = QtGui.QTableWidget(RegistersView)
        self.FormulasTable.setGeometry(QtCore.QRect(430, 60, 211, 391))
        self.FormulasTable.setObjectName("FormulasTable")
        self.FormulasTable.setColumnCount(2)
        self.FormulasTable.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.FormulasTable.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.FormulasTable.setHorizontalHeaderItem(1, item)
        self.AddFormulaButton = QtGui.QPushButton(RegistersView)
        self.AddFormulaButton.setGeometry(QtCore.QRect(450, 20, 171, 31))
        self.AddFormulaButton.setObjectName("AddFormulaButton")

        self.retranslateUi(RegistersView)
        QtCore.QMetaObject.connectSlotsByName(RegistersView)

    def retranslateUi(self, RegistersView):
        RegistersView.setWindowTitle(QtGui.QApplication.translate("RegistersView", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.RegistersTable.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("RegistersView", "Number", None, QtGui.QApplication.UnicodeUTF8))
        self.RegistersTable.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("RegistersView", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.RegistersTable.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("RegistersView", "Hex Value", None, QtGui.QApplication.UnicodeUTF8))
        self.RegistersTable.horizontalHeaderItem(3).setText(QtGui.QApplication.translate("RegistersView", "Function set", None, QtGui.QApplication.UnicodeUTF8))
        self.FormulasTable.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("RegistersView", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.FormulasTable.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("RegistersView", "Value", None, QtGui.QApplication.UnicodeUTF8))
        self.AddFormulaButton.setText(QtGui.QApplication.translate("RegistersView", "Add new formula", None, QtGui.QApplication.UnicodeUTF8))

