
import sys
from PySide import QtCore, QtGui


class MessageBox(QtGui.QDialog):
    

    @staticmethod
    def warningMessage(message):    
        msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Warning,
                "Warning !!!", message,
                QtGui.QMessageBox.NoButton)
        msgBox.addButton("OK", QtGui.QMessageBox.AcceptRole)
        msgBox.exec_()
        # if msgBox.exec_() == QtGui.QMessageBox.AcceptRole:
            # self.warningLabel.setText("OK")
        # else:
            # self.warningLabel.setText("Cancel")