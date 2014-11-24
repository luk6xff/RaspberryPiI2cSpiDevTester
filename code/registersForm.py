
from PySide import QtCore, QtGui
from registersFormUi import Ui_RegitersForm
from styleIcon import StyleIcon



class DeviceDescriptionSheet(QtGui.QWidget):
    
    def __init__(self, parent=None):
        super(DeviceDescriptionSheet, self).__init__(parent)
        self.ui =  Ui_RegitersForm()
        self.ui.setupUi(self)
        self.setItems()
        StyleIcon.setStyleAndIcon(self)
   
    def setItems(self):
        horizontalHeaderLabel = ['Name','Address','Bitmask','Bitmask2']
        self.ui.registersWidget.setRowCount(10)
        self.ui.registersWidget.setColumnCount(3)
        newItem = QtGui.QTableWidgetItem(("%s" % pow(1, 1+1)))
        self.ui.registersWidget.setItem(1, 2, newItem)
        self.ui.registersWidget.setHorizontalHeaderLabels(horizontalHeaderLabel)
 
 
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    myDevice = DeviceDescriptionSheet()
    myDevice.show()
    sys.exit(app.exec_())