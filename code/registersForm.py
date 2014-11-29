
from PySide import QtCore, QtGui
from registersFormUi import Ui_RegitersForm
from styleIcon import StyleIcon
from register8bitMap import Reg8BitMap

D = True    #debug enebled

class DeviceDescriptionSheet(QtGui.QWidget):
    
    def __init__(self, parent=None):
        super(DeviceDescriptionSheet, self).__init__(parent)
        self.ui =  Ui_RegitersForm()
        self.ui.setupUi(self)
        self.registerList= list()  #sth aka MVC dessign pattern, all stuff is located in one list
        self.setItems()
        self.initConnections()
        StyleIcon.setStyleAndIcon(self)
        
   
    def setItems(self):
        horizontalHeaderLabel = ['Name','Address']
        self.ui.registersWidget.setColumnCount(2)
        self.ui.registersWidget.setHorizontalHeaderLabels(horizontalHeaderLabel)
        self.ui.registersWidget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.ui.registersWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
       
        self.addNewRegister()

    def initConnections(self):    # setup all connections of signal and slots
        self.ui.createBitmaskButton.clicked.connect(self.createBitmaskDialog)
        self.ui.addRegisterButton.clicked.connect(self.addNewRegister)
        self.ui.registersWidget.cellClicked.connect(self.reload8BitRegisterView)
        self.ui.registersWidget.cellClicked.connect(self.updateNameOfSelectedRegister) #update Label name of checked register
        self.ui.registersWidget.cellChanged.connect(self.updateNameOfSelectedRegister)
  
        

    
    def addNewRegister(self):

        if D:
            print("List LEN %d" %len(self.registerList))
        if(len(self.registerList) > 0):
            self.registerList[self.lastUsedRow][2].hide()
            #child = self.ui.register8BitHLayout.takeAt(1)
            #del child            
            if D:
                print("Removing Widget")
        self.ui.registersWidget.insertRow(self.ui.registersWidget.rowCount())

        #newItem = QtGui.QTableWidgetItem(("%s" % pow(1, 1+1)))
        #self.ui.registersWidget.setItem(0, 0, newItem)
        
        regTuple= (QtGui.QTableWidgetItem(),QtGui.QTableWidgetItem(),Reg8BitMap()) #one whole row and (Reg name widget item / Addres Widget item / bye widget " 
        self.registerList.append(regTuple)
        
        #view update (all slots and signals are being connected right here )
        self.registerList[-1][2].regValueChanged.connect(self.updateRegisterValue)
        self.registerList[-1][2].regAccessPermissionChanged.connect(self.updateAccessParameters)
        self.ui.register8BitHLayout.addWidget(self.registerList[-1][2])
        self.registerList[-1][2].updateRegisterValue()   
        self.registerList[-1][2].updateRegAccesPermissionParam()
        self.lastUsedRow=self.ui.registersWidget.rowCount()-1 
        self.ui.registersWidget.setItem(self.ui.registersWidget.rowCount()-1 , 0, self.registerList[-1][0])
        self.ui.registersWidget.setItem(self.ui.registersWidget.rowCount()-1 , 1, self.registerList[-1][1])
    # Below all definitions of the slots used by this class
    
    def updateRegisterValue(self,val):
        self.regValue = val
        self.ui.Reg8BitValuePlainTextEdit.setPlainText(str(hex(self.regValue)))
    
    def updateAccessParameters(self,list):
        self.acccessPermisionList= list
        if D:
            print( list )
            
    def updateNameOfSelectedRegister(self,row, column):
        item=self.ui.registersWidget.item(row,0)
        self.ui.nameOfRegLabel.setText(item.text())
    
    def createBitmaskDialog(self):
        bitMaskDialog = BitMaskDialog(self.regValue,self.acccessPermisionList)
        if (bitMaskDialog.exec_()):
            if D:
                print(bitMaskDialog.getModifiedValues()) 
    
    
    def reload8BitRegisterView(self,row,column):
        if(len(self.registerList) > 0):
            self.registerList[self.lastUsedRow][2].hide()
            #child = self.ui.register8BitHLayout.takeAt(1)
            #del child
            if D:
                print("Replace Widget")
                print(self.lastUsedRow)
                print(self.registerList[row][2])
        self.ui.register8BitHLayout.addWidget(self.registerList[row][2])
        self.registerList[row][2].updateRegisterValue()   #TODO 
        self.registerList[row][2].updateRegAccesPermissionParam()
        self.registerList[row][2].show()
        
        self.lastUsedRow=row
        
    



       
class BitMaskDialog(QtGui.QDialog):
    def __init__(self, regVal, accessData, parent=None):
        super(BitMaskDialog, self).__init__(parent)

        tabWidget = QtGui.QTabWidget()
        self.General = GeneralTab(regVal)
        self.Desc = DescriptionTab()
        tabWidget.addTab(self.General, "Bitmask")
        tabWidget.addTab(self.Desc, "Bitmask_Desc")


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
    
    def getModifiedValues(self):
        retValues= [(self.General.bitmaskNameEdit.text()),(self.General.bitmaskValueLabel.text())] #TODO 
        return retValues

        
class GeneralTab(QtGui.QWidget):
    def __init__(self, regVal, parent=None):
        super(GeneralTab, self).__init__(parent)

        bitmaskNameLabel = QtGui.QLabel("Bitmask Name:")
        self.bitmaskNameEdit = QtGui.QLineEdit()

        bitmaskValLabel = QtGui.QLabel("Bitmask Value")
        self.bitmaskValueLabel = QtGui.QLabel(hex(regVal))
        self.bitmaskValueLabel.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Sunken)


        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(bitmaskNameLabel)
        mainLayout.addWidget(self.bitmaskNameEdit)
        mainLayout.addWidget(bitmaskValLabel)
        mainLayout.addWidget(self.bitmaskValueLabel)
   
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
    
    

