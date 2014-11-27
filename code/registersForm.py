
from PySide import QtCore, QtGui
from registersFormUi import Ui_RegitersForm
from styleIcon import StyleIcon
from register8bitMap import Reg8BitMap


class DeviceDescriptionSheet(QtGui.QWidget):
    
    def __init__(self, parent=None):
        super(DeviceDescriptionSheet, self).__init__(parent)
        self.ui =  Ui_RegitersForm()
        self.ui.setupUi(self)
        self.setItems()
        self.initConnections()
        StyleIcon.setStyleAndIcon(self)
   
    def setItems(self):
        horizontalHeaderLabel = ['Name','Address']
        self.ui.registersWidget.setRowCount(10)
        self.ui.registersWidget.setColumnCount(2)
        newItem = QtGui.QTableWidgetItem(("%s" % pow(1, 1+1)))
        self.ui.registersWidget.setItem(1, 2, newItem)
        self.ui.registersWidget.setHorizontalHeaderLabels(horizontalHeaderLabel)
        self.reg8bit = Reg8BitMap()
        self.reg8bit.regValueChanged.connect(self.updateRegisterValue)
        self.ui.register8BitHLayout.addWidget(self.reg8bit)
    
    def updateRegisterValue(self,val):
        self.ui.Reg8BitValuePlainTextEdit.setPlainText(str(val))
    
    def createBitmaskDialog(self):
        bitMaskDialog = BitMaskDialog("AAA")
        bitMaskDialog.exec_()
    
    
    def initConnections(self):
        self.ui.createBitmaskButton.clicked.connect(self.createBitmaskDialog)
    
    
class BitMaskDialog(QtGui.QDialog):
    def __init__(self, fileName, parent=None):
        super(BitMaskDialog, self).__init__(parent)

        tabWidget = QtGui.QTabWidget()
        tabWidget.addTab(GeneralTab(25), "Bitmask")
        tabWidget.addTab(DescriptionTab(), "Bitmask_Desc")


        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(tabWidget)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        self.setWindowTitle("BitMaskDialog")
    
    def setInteger(self):    
        i, ok = QtGui.QInputDialog.getInteger(self,
                "SetBitmaskValue", 25, 0, 100, 1)
        if ok:
            self.integerLabel.setText("%d%%" % i)
    
    def setText(self):
        text, ok = QtGui.QInputDialog.getText(self, "SetBitmaskName",
                "User name:", QtGui.QLineEdit.Normal,
                QtCore.QDir.home().dirName())
        if ok and text != '':
            self.textLabel.setText(text)
            
class GeneralTab(QtGui.QWidget):
    def __init__(self, regVal, parent=None):
        super(GeneralTab, self).__init__(parent)

        bitmaskNameLabel = QtGui.QLabel("Bitmask Name:")
        bitmaskNameEdit = QtGui.QLineEdit()

        bitmaskValLabel = QtGui.QLabel("Bitmask Value")
        bitmaskValueLabel = QtGui.QLabel(str(regVal))
        bitmaskValueLabel.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Sunken)


        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(bitmaskNameLabel)
        mainLayout.addWidget(bitmaskNameEdit)
        mainLayout.addWidget(bitmaskValLabel)
        mainLayout.addWidget(bitmaskValueLabel)
   
        mainLayout.addStretch(1)
        self.setLayout(mainLayout)





class DescriptionTab(QtGui.QWidget):    #TODO here we will add a description of the following tyes of settings for every bitmask
    def __init__(self, parent=None):
        super(DescriptionTab, self).__init__(parent)
        self.textEdit=QtGui.QTextEdit()
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.textEdit)
        mainLayout.addStretch(1)
        self.setLayout(mainLayout) 
 
 
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    myDevice = DeviceDescriptionSheet()
    myDevice.show()
    sys.exit(app.exec_())
    
    

