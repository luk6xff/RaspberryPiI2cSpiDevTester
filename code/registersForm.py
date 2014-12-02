#uszko 26.11.2014
from PySide import QtCore, QtGui
from registersFormUi import Ui_RegitersForm
from styleIcon import StyleIcon
from register8bitMap import Reg8BitMap
from messageBoxWrapper import MessageBox
import re

D = True    #debug enebled

class DeviceDescriptionSheet(QtGui.QWidget):
  
  
    def __init__(self, parent=None):
        super(DeviceDescriptionSheet, self).__init__(parent)
        self.ui =  Ui_RegitersForm()
        self.ui.setupUi(self)
        self.registerList= list()  #sth aka MVC dessign pattern, all stuff is stored in one main list
        self.setItems()
        self.initConnections()
        StyleIcon.setStyleAndIcon(self)
        
   
    def setItems(self):
        horizontalHeaderLabel = ['Name','Address']
        self.ui.registersWidget.setColumnCount(2)
        self.ui.registersWidget.setHorizontalHeaderLabels(horizontalHeaderLabel)
        self.ui.registersWidget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.ui.registersWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.ui.registersWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)#to enable context menu
        self.ui.bitmaskListWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)#to enable context menu
        #Qt::CustomContextMenu, the signal customContextMenuRequested() is emitted.
        #self.ui.bitmaskListWidget.addItem(QtGui.QListWidgetItem("BananaTest"))
        #self.ui.bitmaskListWidget.addItem(QtGui.QListWidgetItem("GrapeTest"))
       
        self.addNewRegister()

        
    def initConnections(self):    # setup all connections of signal and slots
        self.ui.createBitmaskButton.clicked.connect(self.createBitmaskDialog)
        self.ui.saveButton.clicked.connect(self.save)
        self.ui.cancelButton.clicked.connect(self.close)
        self.ui.loadFileButton.clicked.connect(self.open)
        self.ui.addRegisterButton.clicked.connect(self.addNewRegister)
        self.ui.registersWidget.cellClicked.connect(self.reload8BitRegisterView)
        self.ui.registersWidget.cellClicked.connect(self.updateNameOfSelectedRegister) #update Label name of checked register
        self.ui.registersWidget.cellChanged.connect(self.updateNameOfSelectedRegister)
        self.ui.registersWidget.customContextMenuRequested.connect(self.fireUpRegTableWidgetContextMenu) #to enable context menu 
        self.ui.bitmaskListWidget.customContextMenuRequested.connect(self.fireUpBitmaskListWidgetContextMenu)#to enable context menu
        
    
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
        
        regTuple= (QtGui.QTableWidgetItem(),QtGui.QTableWidgetItem(),Reg8BitMap(),list()) #one whole row that contains (Reg name widget item / Addres Widget item / byte widget / list of QListWidgetItems from Bitmas QListWidget (list of dictionaries)   
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
        self.updateBitmaskList(self.ui.registersWidget.rowCount()-1)
    # Below all definitions of the slots used by this class
    
    def updateRegisterValue(self,val):
        self.regValue = val
        self.ui.Reg8BitValuePlainTextEdit.setPlainText(str(hex(self.regValue)))
 
 
    def updateAccessParameters(self,list):
        self.acccessPermisionList= list
        if D:
            print("updateAccessParameters(self,list)")
            print( list )
  
  
    def updateNameOfSelectedRegister(self,row, column):
        item=QtGui.QTableWidgetItem(self.ui.registersWidget.item(row,0))
        self.ui.nameOfRegLabel.setText(item.text())
  
  
    def createBitmaskDialog(self):
        if D:
            print("createBitmaskDialog(self):")
        matchRegVal=re.match(r'[0-9]',(str(self.regValue)),re.I)
        if(matchRegVal):
            if D:
                print(matchRegVal.group())
        else:                                                  #TODO is that needed at all??
            if D:
                print("incorrect register Value")
        if(self.regValue ==0):
            MessageBox.incorrectParamMessage("Cannot create a bitmask with value 0! , Check proper bit(s) and try again") 
            if D:    
                print("Cannot create a bitmask with value 0!")
            return
            
        #check acccessPermisionList whether or not they are equal
        temp = list()
        for attr in range(len(self.acccessPermisionList)):
            if(self.regValue & 1<<attr):
                temp.append(self.acccessPermisionList[attr])
        if(temp[1:] == temp[:-1]):
            if D:
                print("Permission attrs are equal OK")
            accessAttr=temp[0]
        else:
            MessageBox.incorrectParamMessage("Permission attributes are not equal in every Bit. They must be equal, Set them correctly and try again !") 
            if D:    
                print("Permission attrs are different FAILED")
            return
        bitMaskDialog = BitMaskDialog(self.regValue,accessAttr)
        if (bitMaskDialog.exec_()):
            retVal=bitMaskDialog.getModifiedValues()    
            self.registerList[self.ui.registersWidget.currentRow()][2].bitMaskCreated(int(retVal[1],16))
            if D:
                print(retVal)
                print("Bitmask value %d" %(int(retVal[1],16)))
            self.addCreatedBitmask(retVal)
    
    
    def addCreatedBitmask(self,bitmaskParam):
        if(len(bitmaskParam) is not 3):
            return
        newBitMask= {'Name':bitmaskParam[0] , 'Value':bitmaskParam[1] , 'Attr': bitmaskParam[2]}
        if D:
            print("New Bitmask Added")
            print( newBitMask)
            print("currentRow %d" % self.ui.registersWidget.currentRow())
            print("Len of Bitmask ListWidget Before %d" % len(self.registerList[self.ui.registersWidget.currentRow()][3]))
        self.registerList[self.ui.registersWidget.currentRow()][3].append(newBitMask)
        self.updateBitmaskList(self.ui.registersWidget.currentRow())                                              
        if D:
            print("Len of Bitmask ListWidget After %d" % len(self.registerList[self.ui.registersWidget.currentRow()][3]))
            print ("Len Ofthe list %d" % (len(self.registerList[self.ui.registersWidget.currentRow()][3])))
            
            
    def updateBitmaskList(self,regListRow):
        self.ui.bitmaskListWidget.clear() 
        font =QtGui.QFont("Helvetica")
        font.setPointSize(14);
        for i in range(len(self.registerList[regListRow][3])):
            item =  QtGui.QListWidgetItem(self.registerList[regListRow][3][i]['Name']+'   '+
                                             self.registerList[regListRow][3][i]['Value']+'   '+
                                             self.registerList[regListRow][3][i]['Attr'])
            item.setFont(font)
            item.setForeground(QtCore.Qt.red)
            item.setBackground(QtCore.Qt.lightGray)
            self.ui.bitmaskListWidget.addItem(item)
    
    
    def dstrBitMaskTest(self):   ##test method
        self.destroyBitmask(0x3)
    
    
    def destroyBitmask(self,bitmask):
        self.registerList[self.ui.registersWidget.currentRow()][2].bitMaskDestroyed(bitmask)
    
    
    def fireUpBitmaskListWidgetContextMenu(self,position):
        menu= QtGui.QMenu(self.ui.bitmaskListWidget)
        menu.addAction(QtGui.QAction("&Delete", self.ui.bitmaskListWidget, shortcut=QtGui.QKeySequence.Delete,statusTip="remove bitmask", triggered=self.removeBitMask))
        menu.addAction(QtGui.QAction("&Copy", self.ui.bitmaskListWidget, shortcut="Ctrl+C",statusTip="Copy register item", triggered= self.copyRegItem))
        menu.popup(self.ui.bitmaskListWidget.mapToGlobal(position))
        self.positionOfInvokedContextMenu= position
 
 
    def removeBitMask(self):
        if(self.positionOfInvokedContextMenu is None):
            return
        nrOfRowToBeRemoved= self.ui.bitmaskListWidget.row(self.ui.bitmaskListWidget.itemAt(self.positionOfInvokedContextMenu))
        self.positionOfInvokedContextMenu = None
        self.destroyBitmask(int(self.registerList[self.ui.registersWidget.currentRow()][3][nrOfRowToBeRemoved]['Value'],16))
        del self.registerList[self.ui.registersWidget.currentRow()][3][nrOfRowToBeRemoved]
        self.updateBitmaskList(self.ui.registersWidget.currentRow())

 
    def fireUpRegTableWidgetContextMenu(self,position):
        if D:
            print("fireUpRegTableWidgetContectMenu")
        menu= QtGui.QMenu(self.ui.registersWidget)
        menu.addAction(QtGui.QAction("&Delete", self.ui.registersWidget, shortcut=QtGui.QKeySequence.Delete,statusTip="remove register", triggered=self.removeRegisterWidgetTable))
        menu.addAction(QtGui.QAction("&Copy", self.ui.registersWidget, shortcut="Ctrl+C",statusTip="Copy register item", triggered= self.copyRegItem))
        menu.popup(self.ui.registersWidget.mapToGlobal(position))
        self.positionOfInvokedContextMenu= position
   
   
    def removeRegisterWidgetTable(self):
        if(self.positionOfInvokedContextMenu is None):
            return
        nrOfRowToBeRemoved= self.ui.registersWidget.row(self.ui.registersWidget.itemAt(self.positionOfInvokedContextMenu))
        self.positionOfInvokedContextMenu = None
        if(nrOfRowToBeRemoved == 0):
            if D:
                print("Nr of the row =0 , cannot remove this item")
            return

        if D:
            print("removed")
            print("nrOfRowToBeRemoved %d" %nrOfRowToBeRemoved)
        self.removeRegister(nrOfRowToBeRemoved)
    

    
    def removeRegister(self,regRow):
        self.ui.registersWidget.removeRow(regRow)
        #self.ui.register8BitHLayout.removeWidget(self.registerList[regRow][2])
        #self.ui.register8BitHLayout.layout().removeWidget(self.registerList[regRow][2])
        #del self.registerList[regRow][2]
        
        #item =self.ui.register8BitHLayout.itemAt(0)
        #self.ui.register8BitHLayout.removeWidget(item.widget())
        #del item
        
        #layout = self.ui.register8BitHLayout.layout().takeAt(0)
        #layout.deleteLater()
        self.registerList[regRow][2].hide()          #TODO
        #self.clearLayout(self.ui.register8BitHLayout.layout())
        print("Adddr:",self.registerList[regRow][2])
        #child =self.ui.register8BitHLayout.takeAt(0)
        #del child
        #self.ui.register8BitHLayout.update()
        #child = self.ui.register8BitHLayout.itemAt(0)
        #del child
        del self.registerList[regRow]        
        self.updateBitmaskList(regRow-1)
        self.registerList[regRow-1][2].updateRegisterValue()   
        self.registerList[regRow-1][2].updateRegAccesPermissionParam()
        self.registerList[regRow-1][2].show()
        self.lastUsedRow=self.ui.registersWidget.rowCount()-1 
        

        #self.lastUsedRow=len(self.registerList)-1
    def clearLayout(layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                clearLayout(child.layout())
    
    
    def copyRegItem(self):
        print("copied") #TODO
    
    
    def reload8BitRegisterView(self,row,column):
        if(len(self.registerList) > 0):
            self.registerList[self.lastUsedRow][2].hide()
            #child = self.ui.register8BitHLayout.takeAt(1)
            #del child
            if D:
                print("reload8BitRegisterView(self,row,column)")
                print(self.lastUsedRow)
                print(self.registerList[row][2])
        self.ui.register8BitHLayout.addWidget(self.registerList[row][2])
        self.registerList[row][2].updateRegisterValue()   
        self.registerList[row][2].updateRegAccesPermissionParam()
        self.registerList[row][2].show()
        self.updateBitmaskList(row)
        self.lastUsedRow=row
        
    #save method
    def save(self):
        filename, filtr = QtGui.QFileDialog.getSaveFileName(self,
                "Choose a file name", '.', "rd (*.rd)")
        if not filename:
            return

        file = QtCore.QFile(filename)
        if not file.open(QtCore.QIODevice.WriteOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, "I2C_SPI_CHECKER",
                    "Cannot write file %s:\n%s." % (filename, file.errorString()))
            return
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        self.generateXML(file)
        QtGui.QApplication.restoreOverrideCursor()
        #self.statusBar().showMessage("Saved '%s'" % filename, 2000) 
        
        # out = QtCore.QTextStream(file)
        # QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        # out << self.textEdit.toHtml()
        # QtGui.QApplication.restoreOverrideCursor()

        # self.statusBar().showMessage("Saved '%s'" % filename, 2000)    
    
    
    def generateXML(self,file):
    #TODO ADD auto checking of correctness of all parameters !!!!
        xmlWriter = QtCore.QXmlStreamWriter()
        xmlWriter.setDevice(file)
        xmlWriter.setAutoFormatting ( True )
        xmlWriter.setAutoFormattingIndent(1) 
        xmlWriter.writeStartDocument()
        xmlWriter.writeStartElement("device")
        xmlWriter.writeStartElement("name")
        xmlWriter.writeCharacters(self.ui.deviceNameTextEdit.toPlainText())
        xmlWriter.writeEndElement()
        xmlWriter.writeStartElement("address")
        xmlWriter.writeCharacters(self.ui.addressTextEdit.toPlainText())
        xmlWriter.writeEndElement()
        xmlWriter.writeStartElement("registers")
        
        for i in range(len(self.registerList)):
            xmlWriter.writeStartElement("register")
            xmlWriter.writeStartElement("name")
            xmlWriter.writeCharacters(self.registerList[i][0].text())
            xmlWriter.writeEndElement()
            xmlWriter.writeStartElement("address")
            xmlWriter.writeCharacters(self.registerList[i][1].text())
            xmlWriter.writeEndElement()
            xmlWriter.writeStartElement("bitmasks")
            for j in range(len(self.registerList[i][3])):
                xmlWriter.writeStartElement("bitmask")
                xmlWriter.writeStartElement("name")
                xmlWriter.writeCharacters(self.registerList[i][3][j]['Name'])
                xmlWriter.writeEndElement()
                xmlWriter.writeStartElement("mask")
                xmlWriter.writeCharacters(self.registerList[i][3][j]['Value'])
                xmlWriter.writeEndElement()
                xmlWriter.writeStartElement("access_attr")
                xmlWriter.writeCharacters(self.registerList[i][3][j]['Attr'])
                xmlWriter.writeEndElement()
                xmlWriter.writeEndElement()
            
            xmlWriter.writeEndElement()
            xmlWriter.writeEndElement()
        
        xmlWriter.writeEndElement()
        xmlWriter.writeEndElement()
        xmlWriter.writeEndDocument()
     
    def open(self):
        self.readXML()
        
    def readXML(self):
        options = QtGui.QFileDialog.Options()
        filename, filtr = QtGui.QFileDialog.getOpenFileName(self,
                "Choose a file name", '.', "rd (*.rd)", "", options)
        if filename:
            file = QtCore.QFile(filename)
            if not file.open(QtCore.QIODevice.ReadOnly | QtCore.QIODevice.Text):
                QtGui.QMessageBox.critical(self, "read I2C_SPI_CHECKER xml file ERROR",
                    "Couldn't open file %s:\n%s." % (filename, file.errorString()))
                return      
        else:           
            return
        xmlReader = QtCore.QXmlStreamReader(file)
        regMap=list()
       
        #regMap.append(regTuple)
        deviceName = str()
        deviceAddr = str()
        if D:
            print("INIT!, devName and Addr")

        while( (not xmlReader.atEnd()) and  (not xmlReader.hasError())):
            xmlReader.readNext() #just skip the intro
            if(xmlReader.isStartDocument()):
                continue
            if(xmlReader.isStartElement()):
                if(xmlReader.name()== 'device'):
                    continue
                elif(xmlReader.name()=='name'):
                    deviceName= self.readElementData(xmlReader)
                elif(xmlReader.name()=='address'):
                    deviceAddr = self.readElementData(xmlReader)
                elif(xmlReader.name()=='registers'):
                    continue
                elif(xmlReader.name()=='register'):
                    regMap.append(self.parseRegister(xmlReader))
                    continue
                    
        #print("ERROR! , incompatible xml file")
        if D:
            print("DEVICE_NAME %s" %deviceName, "DEVICE_ADDR %s" %deviceAddr)
     
    def readElementData(self,xmlReader):
        if(not xmlReader.isStartElement()):
            return
        if D:
            print("element Name %s" % xmlReader.name())
        xmlReader.readNext()
        if(not xmlReader.isCharacters()):
            return
        return xmlReader.text()

     
    def parseRegister(self,xmlReader):
        regTuple= (str(),str(),str(),list())
        if((not xmlReader.isStartElement())&&(xmlReader.name=='register' )):
            return regTuple
        
        return  regTuple= (QtGui.QTableWidgetItem(),QtGui.QTableWidgetItem(),Reg8BitMap(),list())
    
    
    
    #think it over
    # class XmlRegisterFile:
    # def __init__(self, list
    
     
class BitMaskDialog(QtGui.QDialog):
    def __init__(self, regVal, accessAttr, parent=None):
        super(BitMaskDialog, self).__init__(parent)

        tabWidget = QtGui.QTabWidget()
        self.General = GeneralTab(regVal,accessAttr)
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
   
   
    def getModifiedValues(self):
        retValues= [(self.General.bitmaskNameEdit.text()),(self.General.bitmaskValueLabel.text()),(self.General.accessAttr.text())] 
        return retValues
        

        
class GeneralTab(QtGui.QWidget):
    def __init__(self, regVal, accessAttr,parent=None):
        super(GeneralTab, self).__init__(parent)

        bitmaskNameLabel = QtGui.QLabel("Bitmask Name:")
        self.bitmaskNameEdit = QtGui.QLineEdit()

        bitmaskValLabel = QtGui.QLabel("Bitmask Value")
        self.bitmaskValueLabel = QtGui.QLabel(hex(regVal))
        self.bitmaskValueLabel.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Sunken)
        
        accessAttrLabel = QtGui.QLabel("Access attribute")
        self.accessAttr = QtGui.QLabel(accessAttr)
        self.accessAttr.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Sunken)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(bitmaskNameLabel)
        mainLayout.addWidget(self.bitmaskNameEdit)
        mainLayout.addWidget(bitmaskValLabel)
        mainLayout.addWidget(self.bitmaskValueLabel)
        mainLayout.addWidget(accessAttrLabel)
        mainLayout.addWidget(self.accessAttr)
   
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
    
    

