# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uiRegistersView.ui'
#
# Created: Thu Dec 11 00:37:22 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_RegistersView(object):
    def setupUi(self, RegistersView):
        RegistersView.setObjectName("RegistersView")
        RegistersView.resize(749, 526)
        self.groupBox = QtGui.QGroupBox(RegistersView)
        self.groupBox.setGeometry(QtCore.QRect(10, 40, 421, 111))
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayoutWidget = QtGui.QWidget(self.groupBox)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 20, 411, 81))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.bitmaskTableWidget = QtGui.QTableWidget(self.horizontalLayoutWidget)
        self.bitmaskTableWidget.setObjectName("bitmaskTableWidget")
        self.bitmaskTableWidget.setColumnCount(3)
        self.bitmaskTableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.bitmaskTableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.bitmaskTableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.bitmaskTableWidget.setHorizontalHeaderItem(2, item)
        self.horizontalLayout.addWidget(self.bitmaskTableWidget)
        self.updateCommandLinkButton = QtGui.QCommandLinkButton(self.horizontalLayoutWidget)
        self.updateCommandLinkButton.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(8)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.updateCommandLinkButton.sizePolicy().hasHeightForWidth())
        self.updateCommandLinkButton.setSizePolicy(sizePolicy)
        self.updateCommandLinkButton.setMaximumSize(QtCore.QSize(93, 42))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setWeight(75)
        font.setItalic(True)
        font.setBold(True)
        self.updateCommandLinkButton.setFont(font)
        self.updateCommandLinkButton.setObjectName("updateCommandLinkButton")
        self.horizontalLayout.addWidget(self.updateCommandLinkButton)
        spacerItem = QtGui.QSpacerItem(0, 16, QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.groupBox_2 = QtGui.QGroupBox(RegistersView)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 150, 421, 371))
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayoutWidget = QtGui.QWidget(self.groupBox_2)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 20, 411, 351))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.RegistersTable = QtGui.QTableWidget(self.verticalLayoutWidget)
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
        self.verticalLayout.addWidget(self.RegistersTable)
        self.UpdateRegisterButton = QtGui.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.UpdateRegisterButton.sizePolicy().hasHeightForWidth())
        self.UpdateRegisterButton.setSizePolicy(sizePolicy)
        self.UpdateRegisterButton.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.UpdateRegisterButton.setObjectName("UpdateRegisterButton")
        self.verticalLayout.addWidget(self.UpdateRegisterButton)
        self.groupBox_3 = QtGui.QGroupBox(RegistersView)
        self.groupBox_3.setGeometry(QtCore.QRect(430, 40, 311, 481))
        self.groupBox_3.setObjectName("groupBox_3")
        self.FormulaText = QtGui.QPlainTextEdit(self.groupBox_3)
        self.FormulaText.setGeometry(QtCore.QRect(10, 20, 291, 41))
        self.FormulaText.setObjectName("FormulaText")
        self.AddFormulaButton = QtGui.QPushButton(self.groupBox_3)
        self.AddFormulaButton.setGeometry(QtCore.QRect(80, 70, 181, 31))
        self.AddFormulaButton.setObjectName("AddFormulaButton")
        self.verticalLayoutWidget_2 = QtGui.QWidget(self.groupBox_3)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 110, 291, 371))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.FormulasTable = QtGui.QTableWidget(self.verticalLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.FormulasTable.sizePolicy().hasHeightForWidth())
        self.FormulasTable.setSizePolicy(sizePolicy)
        self.FormulasTable.setObjectName("FormulasTable")
        self.FormulasTable.setColumnCount(3)
        self.FormulasTable.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.FormulasTable.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.FormulasTable.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.FormulasTable.setHorizontalHeaderItem(2, item)
        self.verticalLayout_3.addWidget(self.FormulasTable)
        self.devNameLabel = QtGui.QLabel(RegistersView)
        self.devNameLabel.setGeometry(QtCore.QRect(10, 10, 211, 31))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.devNameLabel.sizePolicy().hasHeightForWidth())
        self.devNameLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("MS PGothic")
        font.setPointSize(15)
        font.setWeight(75)
        font.setUnderline(True)
        font.setStrikeOut(False)
        font.setBold(True)
        self.devNameLabel.setFont(font)
        self.devNameLabel.setMouseTracking(False)
        self.devNameLabel.setAcceptDrops(False)
        self.devNameLabel.setInputMethodHints(QtCore.Qt.ImhPreferUppercase)
        self.devNameLabel.setText("")
        self.devNameLabel.setTextFormat(QtCore.Qt.PlainText)
        self.devNameLabel.setScaledContents(True)
        self.devNameLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.devNameLabel.setWordWrap(False)
        self.devNameLabel.setObjectName("devNameLabel")
        self.devAddrLabel = QtGui.QLabel(RegistersView)
        self.devAddrLabel.setGeometry(QtCore.QRect(210, 10, 211, 31))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.devAddrLabel.sizePolicy().hasHeightForWidth())
        self.devAddrLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("MS PGothic")
        font.setPointSize(15)
        font.setWeight(75)
        font.setUnderline(True)
        font.setStrikeOut(False)
        font.setBold(True)
        self.devAddrLabel.setFont(font)
        self.devAddrLabel.setMouseTracking(False)
        self.devAddrLabel.setAcceptDrops(False)
        self.devAddrLabel.setInputMethodHints(QtCore.Qt.ImhPreferUppercase)
        self.devAddrLabel.setText("")
        self.devAddrLabel.setTextFormat(QtCore.Qt.PlainText)
        self.devAddrLabel.setScaledContents(True)
        self.devAddrLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.devAddrLabel.setWordWrap(False)
        self.devAddrLabel.setObjectName("devAddrLabel")

        self.retranslateUi(RegistersView)
        QtCore.QMetaObject.connectSlotsByName(RegistersView)

    def retranslateUi(self, RegistersView):
        RegistersView.setWindowTitle(QtGui.QApplication.translate("RegistersView", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("RegistersView", "Bitmasks", None, QtGui.QApplication.UnicodeUTF8))
        self.bitmaskTableWidget.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("RegistersView", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.bitmaskTableWidget.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("RegistersView", "Mask", None, QtGui.QApplication.UnicodeUTF8))
        self.bitmaskTableWidget.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("RegistersView", "Value", None, QtGui.QApplication.UnicodeUTF8))
        self.updateCommandLinkButton.setText(QtGui.QApplication.translate("RegistersView", "Update ", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("RegistersView", "Registers", None, QtGui.QApplication.UnicodeUTF8))
        self.RegistersTable.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("RegistersView", "Addr", None, QtGui.QApplication.UnicodeUTF8))
        self.RegistersTable.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("RegistersView", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.RegistersTable.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("RegistersView", "Hex Value", None, QtGui.QApplication.UnicodeUTF8))
        self.RegistersTable.horizontalHeaderItem(3).setText(QtGui.QApplication.translate("RegistersView", "Function set", None, QtGui.QApplication.UnicodeUTF8))
        self.UpdateRegisterButton.setText(QtGui.QApplication.translate("RegistersView", "Update register", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("RegistersView", "Formulas", None, QtGui.QApplication.UnicodeUTF8))
        self.AddFormulaButton.setText(QtGui.QApplication.translate("RegistersView", "Add new formula", None, QtGui.QApplication.UnicodeUTF8))
        self.FormulasTable.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("RegistersView", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.FormulasTable.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("RegistersView", "Value", None, QtGui.QApplication.UnicodeUTF8))
        self.FormulasTable.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("RegistersView", "Formula", None, QtGui.QApplication.UnicodeUTF8))

