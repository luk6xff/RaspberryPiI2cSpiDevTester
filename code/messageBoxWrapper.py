
import sys
from PySide import QtCore, QtGui




class MessageBox(QtGui.QDialog):
    

    @staticmethod
    def warningMessage(message,firstAcceptButtonText, acceptMethod, acceptMethodArgs):    
        msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Warning,
                "Warning !!!", message,
                QtGui.QMessageBox.NoButton|QtGui.QMessageBox.Cancel)
        msgBox.addButton(firstAcceptButtonText, QtGui.QMessageBox.AcceptRole)
        #msgBox.exec_()
        if msgBox.exec_() == QtGui.QMessageBox.AcceptRole:
            if acceptMethod is not None: 
                acceptMethod(*acceptMethodArgs)
        # else:
            # rejectMethod(*rejectMethodArgs)