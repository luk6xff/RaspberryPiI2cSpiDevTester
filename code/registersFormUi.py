# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uiRegisterForm.ui'
#
# Created: Mon Nov 24 01:37:09 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_RegitersForm(object):
    def setupUi(self, RegitersForm):
        RegitersForm.setObjectName("RegitersForm")
        RegitersForm.resize(683, 433)
        self.registersWidget = QtGui.QTableWidget(RegitersForm)
        self.registersWidget.setGeometry(QtCore.QRect(40, 80, 541, 251))
        self.registersWidget.setObjectName("registersWidget")
        self.registersWidget.setColumnCount(0)
        self.registersWidget.setRowCount(0)
        self.horizontalLayoutWidget = QtGui.QWidget(RegitersForm)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(40, 10, 541, 61))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.deviceNameLabel = QtGui.QLabel(self.horizontalLayoutWidget)
        self.deviceNameLabel.setObjectName("deviceNameLabel")
        self.horizontalLayout.addWidget(self.deviceNameLabel)
        self.deviceNameTextEdit = QtGui.QTextEdit(self.horizontalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.deviceNameTextEdit.sizePolicy().hasHeightForWidth())
        self.deviceNameTextEdit.setSizePolicy(sizePolicy)
        self.deviceNameTextEdit.setMinimumSize(QtCore.QSize(7, 5))
        self.deviceNameTextEdit.setMaximumSize(QtCore.QSize(1677, 1677))
        self.deviceNameTextEdit.setFrameShadow(QtGui.QFrame.Plain)
        self.deviceNameTextEdit.setObjectName("deviceNameTextEdit")
        self.horizontalLayout.addWidget(self.deviceNameTextEdit)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.addressLabel = QtGui.QLabel(self.horizontalLayoutWidget)
        self.addressLabel.setObjectName("addressLabel")
        self.horizontalLayout.addWidget(self.addressLabel)
        self.addressTextEdit = QtGui.QTextEdit(self.horizontalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addressTextEdit.sizePolicy().hasHeightForWidth())
        self.addressTextEdit.setSizePolicy(sizePolicy)
        self.addressTextEdit.setMinimumSize(QtCore.QSize(7, 5))
        self.addressTextEdit.setMaximumSize(QtCore.QSize(1677, 1677))
        self.addressTextEdit.setFrameShadow(QtGui.QFrame.Plain)
        self.addressTextEdit.setObjectName("addressTextEdit")
        self.horizontalLayout.addWidget(self.addressTextEdit)
        spacerItem1 = QtGui.QSpacerItem(200, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.saveButton = QtGui.QPushButton(RegitersForm)
        self.saveButton.setGeometry(QtCore.QRect(470, 380, 75, 23))
        self.saveButton.setObjectName("saveButton")
        self.cancelButton = QtGui.QPushButton(RegitersForm)
        self.cancelButton.setGeometry(QtCore.QRect(580, 380, 75, 23))
        self.cancelButton.setObjectName("cancelButton")

        self.retranslateUi(RegitersForm)
        QtCore.QMetaObject.connectSlotsByName(RegitersForm)

    def retranslateUi(self, RegitersForm):
        RegitersForm.setWindowTitle(QtGui.QApplication.translate("RegitersForm", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.deviceNameLabel.setText(QtGui.QApplication.translate("RegitersForm", "Device name:", None, QtGui.QApplication.UnicodeUTF8))
        self.addressLabel.setText(QtGui.QApplication.translate("RegitersForm", "7 bit Address:", None, QtGui.QApplication.UnicodeUTF8))
        self.saveButton.setText(QtGui.QApplication.translate("RegitersForm", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("RegitersForm", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

