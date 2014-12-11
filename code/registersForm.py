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
        self.ui.registersWidget.setColumnWidth(0,132)
        self.ui.registersWidget.horizontalHeader().setStretchLastSection(True)
        self.ui.registersWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)#to enable context menu
        self.ui.bitmaskListWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)#to enable context menu
        #Qt::CustomContextMenu, the signal customContextMenuRequested() is emitted.
       
        self.addNewRegister()

        
    def initConnections(self):    # setup all connections of signal and slots
        self.ui.createBitmaskButton.clicked.connect(self.__createBitmaskDialog)
        self.ui.saveButton.clicked.connect(self.__save)
        self.ui.cancelButton.clicked.connect(self.close)
        self.ui.loadFileButton.clicked.connect(self.__openXMLFile)
        self.ui.addRegisterButton.clicked.connect(self.addNewRegister)
        self.ui.registersWidget.cellClicked.connect(self.__reload8BitRegisterView)
        self.ui.registersWidget.cellClicked.connect(self.__updateNameOfSelectedRegister) #update Label name of checked register
        self.ui.registersWidget.cellChanged.connect(self.__updateNameOfSelectedRegister)
        self.ui.registersWidget.customContextMenuRequested.connect(self.__fireUpRegTableWidgetContextMenu) #to enable context menu 
        self.ui.bitmaskListWidget.customContextMenuRequested.connect(self.__fireUpBitmaskListWidgetContextMenu)#to enable context menu
        
    
    def addNewRegister(self,regList=None):

        if D:    
            print("List LEN %d" %len(self.registerList))
        if(len(self.registerList) > 0):
            self.registerList[self.lastUsedRow][2].hide()
            if D:
                print("Removing Widget")
        self.ui.registersWidget.insertRow(self.ui.registersWidget.rowCount())
        if(regList is not None): #it means that we are to load new xml pattern 
            singleRegList= (QtGui.QTableWidgetItem(regList[0]),QtGui.QTableWidgetItem(regList[1]),Reg8BitMap(),list())
        else:
            singleRegList= [QtGui.QTableWidgetItem(),QtGui.QTableWidgetItem(),Reg8BitMap(),list()] #one whole row that contains (Reg name widget item / Addres Widget item / byte widget / list of QListWidgetItems from Bitmas QListWidget (list of dictionaries)   
        self.registerList.append(singleRegList)
        #view update (all slots and signals are being connected right here )
        self.registerList[-1][2].regValueChanged.connect(self.__updateRegisterValue)
        self.registerList[-1][2].regAccessPermissionChanged.connect(self.__updateAccessParameters)
        self.ui.register8BitHLayout.addWidget(self.registerList[-1][2])
        if(regList is not None):
            for i in range(len(regList[2])):
                self.__addCreatedBitmask(regList[2][i])
          
        self.registerList[-1][2].updateRegAccesPermissionParam()
        self.ui.registersWidget.setItem(self.ui.registersWidget.rowCount()-1 , 0, self.registerList[-1][0])
        self.ui.registersWidget.setItem(self.ui.registersWidget.rowCount()-1 , 1, self.registerList[-1][1])
        self.__updateBitmaskList(self.ui.registersWidget.rowCount()-1)
        self.registerList[-1][2].updateRegisterValue()
        self.lastUsedRow=self.ui.registersWidget.rowCount()-1
        self.__reload8BitRegisterView(self.ui.registersWidget.rowCount()-1,0)
        
        
        
    # Below all definitions of the slots used by this class
    def __updateRegisterValue(self,val):
        self.regValue = val
        self.ui.Reg8BitValuePlainTextEdit.setPlainText("0x%02x" %(self.regValue))
 
 
    def __updateAccessParameters(self,list):
        self.acccessPermisionList= list
        if D:
            print("__updateAccessParameters(self,list)")
            print( list )
  
    
    def __updateRegAccessAttributes(self,attrList,regNr):  
        if(attrList is None or regNr<0):
            return 
        self.registerList[regNr][2].setRegAccesPermissionParam(attrList)
        
    
    def __updateNameOfSelectedRegister(self,row, column):
        item=QtGui.QTableWidgetItem(self.ui.registersWidget.item(row,0))
        self.ui.nameOfRegLabel.setText(item.text())
  
  
    def __createBitmaskDialog(self):
        if D:
            print("__createBitmaskDialog(self):")
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
            self.__addCreatedBitmask(retVal)
    
    
    def __addCreatedBitmask(self,bitmaskParam):
        if(len(bitmaskParam) is not 3):
            return
        self.registerList[self.ui.registersWidget.currentRow()][2].bitMaskCreated(int(bitmaskParam['Value'],16))
        if D:
            print("Bitmask value %d" %(int(bitmaskParam['Value'],16)))
        newBitMask= {'Name':bitmaskParam['Name'] , 'Value':bitmaskParam['Value'] , 'Attr': bitmaskParam['Attr']}
        # if D:
            # print("New Bitmask Added")
        self.registerList[self.ui.registersWidget.currentRow()][3].append(newBitMask)
        self.__updateBitmaskList(self.ui.registersWidget.currentRow())                                              
        # if D:
            # print("Len of Bitmask ListWidget After %d" % len(self.registerList[self.ui.registersWidget.currentRow()][3]))
            # print ("Len Ofthe list %d" % (len(self.registerList[self.ui.registersWidget.currentRow()][3])))
            
    def __updateBitmaskList(self,regListRow):
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
    
    
    
    def __destroyBitmask(self,bitmask,regRow):
        if regRow<self.ui.registersWidget.rowCount()-1:
            return
        self.registerList[regRow][2].bitMaskDestroyed(bitmask)
    
    
    def __fireUpBitmaskListWidgetContextMenu(self,position):
        menu= QtGui.QMenu(self.ui.bitmaskListWidget)
        menu.addAction(QtGui.QAction("&Delete", self.ui.bitmaskListWidget, shortcut=QtGui.QKeySequence.Delete,statusTip="remove bitmask", triggered=self.__removeBitMask))
        menu.addAction(QtGui.QAction("&Copy", self.ui.bitmaskListWidget, shortcut="Ctrl+C",statusTip="Copy register item", triggered= self.__copyRegItem))
        menu.popup(self.ui.bitmaskListWidget.mapToGlobal(position))
        self.positionOfInvokedContextMenu= position
 
 
    def __removeBitMask(self):
        if(self.positionOfInvokedContextMenu is None or self.ui.bitmaskListWidget.count() ==0):
            return
        nrOfRowToBeRemoved= self.ui.bitmaskListWidget.row(self.ui.bitmaskListWidget.itemAt(self.positionOfInvokedContextMenu))
        self.positionOfInvokedContextMenu = None
        self.__destroyBitmask(int(self.registerList[self.ui.registersWidget.currentRow()][3][nrOfRowToBeRemoved]['Value'],16),self.ui.registersWidget.currentRow())
        del self.registerList[self.ui.registersWidget.currentRow()][3][nrOfRowToBeRemoved]
        self.__updateBitmaskList(self.ui.registersWidget.currentRow())
    
    def __removeAllBitMasksFromRegister(self,row):
        if(row<self.ui.registersWidget.rowCount()-1):
            return       
        for i in range(self.ui.bitmaskListWidget.count()):
            self.__destroyBitmask(int(self.registerList[row][3][i]['Value'],16),row)
            del self.registerList[self.ui.registersWidget.currentRow()][3][i]
        self.ui.bitmaskListWidget.clear() 
        #self.__updateBitmaskList(row)

 
    def __fireUpRegTableWidgetContextMenu(self,position):
        if D:
            print("fireUpRegTableWidgetContectMenu")
        menu= QtGui.QMenu(self.ui.registersWidget)
        menu.addAction(QtGui.QAction("&Delete", self.ui.registersWidget, shortcut=QtGui.QKeySequence.Delete,statusTip="remove register", triggered=self.__removeRegisterWidgetTableFromContextMenu))
        menu.addAction(QtGui.QAction("&Copy", self.ui.registersWidget, shortcut="Ctrl+C",statusTip="Copy register item", triggered= self.__copyRegItem))
        menu.popup(self.ui.registersWidget.mapToGlobal(position))
        self.positionOfInvokedContextMenu= position
   
   
    def __removeRegisterWidgetTableFromContextMenu(self):
        if(self.positionOfInvokedContextMenu is None):
            return
        nrOfRowToBeRemoved= self.ui.registersWidget.row(self.ui.registersWidget.itemAt(self.positionOfInvokedContextMenu))
        self.positionOfInvokedContextMenu = None
        if(nrOfRowToBeRemoved <0 ):
            if D:
                print("Nr of the row <0 , cannot remove this item")
            return

        if D:
            print("removed")
            print("nrOfRowToBeRemoved %d" %nrOfRowToBeRemoved)
        self.__removeRegister(nrOfRowToBeRemoved)
    

    
    def __removeRegister(self,regRow):
        if(regRow<0):
            raise Exception("regRow less than ZERO ERROR")
        
        self.ui.registersWidget.removeRow(regRow)
        self.registerList[regRow][2].hide()          #TODO
        #self.clearLayout(self.ui.register8BitHLayout.layout())
        if D:
            print("REMOVED: :",self.registerList[regRow][2])
        del self.registerList[regRow]
        if(regRow>0):                           #show the last not removed row
            self.__updateBitmaskList(regRow-1)
            self.registerList[regRow-1][2].updateRegisterValue()   
            self.registerList[regRow-1][2].updateRegAccesPermissionParam()
            self.registerList[regRow-1][2].show()
        self.lastUsedRow=regRow-1

            
        
     
    
    
    def removeAllRegisters(self):
        nrOfRows= len(self.registerList)-1
        while(nrOfRows>-1):
            self.__removeRegister(nrOfRows) 
            nrOfRows=nrOfRows-1
        self.firstRowFlag=False   
        
        
       
    def clearLayout(layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                clearLayout(child.layout())
    
    
    def __copyRegItem(self):
        print("copied") #TODO
    
    
    def clearRegister(self,row):
        #self.registerList[row][0]=
        return
        
    
    def __reload8BitRegisterView(self,row,column):
        if(len(self.registerList) > 0):
            self.registerList[self.lastUsedRow][2].hide()
            #child = self.ui.register8BitHLayout.takeAt(1)
            #del child
            if D:
                print("__reload8BitRegisterView(self,row,column)")
                print("self.lastUsedRow",self.lastUsedRow)
                print("self.registerList[row][2]", row, "   " ,self.registerList[row][2])
        self.ui.register8BitHLayout.addWidget(self.registerList[row][2])
        self.registerList[row][2].updateRegisterValue()   
        self.registerList[row][2].updateRegAccesPermissionParam()
        self.registerList[row][2].show()
        self.__updateBitmaskList(row)
        self.lastUsedRow=row
    
    def setDeviceName(self,name):
        self.ui.deviceNameTextEdit.setText(name)
    def getDeviceName(self):
        return self.ui.deviceNameTextEdit.toPlainText()
    def setDeviceAddr(self,name):
        self.ui.addressTextEdit.setText(name)
    def getDeviceAddr(self):
        return self.ui.addressTextEdit.toPlainText()
        
     

    def checkParamCorrectnessBeforeSave(self):
        addrPattern= re.compile('0x[0-9a-fA-F][0-9a-fA-F]'); 
        for i in range(len(self.registerList)):
            m = re.search(addrPattern,self.registerList[i][1].text())
            if m:
                if D:
                    print("found a match:", m.group(0))
            else:
                if D:
                    print("PATTERN has not been found ",self.registerList[i][1].text())
                QtGui.QMessageBox.critical(self, "I2C_SPI_CHECKER incorrect value",
                    "Register ' %s ': contains incorrect format of the address: ' %s '\n Address must be typed in the following format: 0xFF\n Correct it and try again!" % (self.registerList[i][0].text(), self.registerList[i][1].text()))
                return False
        return True

     
    #__save method
    def __save(self):
        if D:
            print("__save INVOKED")
        if((self.checkParamCorrectnessBeforeSave()) is False): 
            return
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        xml = XmlRegister(self.registerList,self.getDeviceName(),self.getDeviceAddr())
        xml.generateXML()
        QtGui.QApplication.restoreOverrideCursor()
        # self.statusBar().showMessage("__saved '%s'" % filename, 2000)    
    
    
    def __openXMLFile(self):
        xml = XmlRegister()
        regMap,devName,devAddr= xml.readXML()
        if((regMap is not None) and (devName is not None) and (devAddr is not None)):
            self.__updateUiWithNewXml(regMap,devName,devAddr)

    def __updateUiWithNewXml(self, regList,deviceName,deviceAddr):
        #if(len(regList)!=3):
        #    return
        self.removeAllRegisters()
        self.setDeviceName(deviceName)
        self.setDeviceAddr(deviceAddr)       
        for i in range(len(regList)):
            #self.__updateAccessParameters(regList[i][3])
            self.addNewRegister(regList[i])
            self.__updateRegAccessAttributes(regList[i][3],i)

        
        
        
    #private class for operating on XML file 
class XmlRegister(QtGui.QWidget):  #inheits QWidget to operate on QFileDialogs correctly

    def __init__(self,regList=None,devName=None,devAddr=None, parent=None):
        super(XmlRegister, self).__init__(parent)
        self.registerList= regList
        self.devAddr= devAddr
        self.devName= devName
    
    def __openWriteFileDialog(self):
        filename, filtr = QtGui.QFileDialog.getSaveFileName(self,
                "Choose a file name", '.', "rd (*.rd)")
        if not filename:
            return

        file = QtCore.QFile(filename)
        if not file.open(QtCore.QIODevice.WriteOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, "I2C_SPI_CHECKER",
                    "Cannot write file %s:\n%s." % (filename, file.errorString()))
            return
        else:
            return file

    
    def generateXML(self):
    #TODO ADD auto checking of correctness of all parameters !!!!
    
        if(self.registerList==None or self.devName==None or self.devAddr==None):
            if D:
                print("INCORRECT initialisation of the xml object")
            return
        
        file = self.__openWriteFileDialog()
        if(not file):
            return

        xmlWriter = QtCore.QXmlStreamWriter()
        xmlWriter.setDevice(file)
        xmlWriter.setAutoFormatting ( True )
        xmlWriter.setAutoFormattingIndent(1) 
        xmlWriter.writeStartDocument()
        xmlWriter.writeStartElement("device")
        xmlWriter.writeStartElement("name")
        xmlWriter.writeCharacters(self.devName)
        xmlWriter.writeEndElement()
        xmlWriter.writeStartElement("address")
        xmlWriter.writeCharacters(self.devAddr)
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
            access_list= self.registerList[i][2].getRegAccessPerametersList()
            xmlWriter.writeStartElement("byte_access_attr")
            for i in range(len(access_list)):
                xmlWriter.writeStartElement("access_attr")
                xmlWriter.writeCharacters(access_list[i])
                xmlWriter.writeEndElement()
            xmlWriter.writeEndElement()
            xmlWriter.writeEndElement()
        xmlWriter.writeEndElement()
        xmlWriter.writeEndElement()
        xmlWriter.writeEndDocument()



    def readXML(self,fileName=None):
        self.__respondNone = [None,None,None]
        if(fileName is None):
            options = QtGui.QFileDialog.Options()
            filename, filtr = QtGui.QFileDialog.getOpenFileName(self,
                "Choose a file name", '.', "rd (*.rd)", "", options)
        if filename:
            file = QtCore.QFile(filename)
            if not file.open(QtCore.QIODevice.ReadOnly | QtCore.QIODevice.Text):
                QtGui.QMessageBox.critical(self, "read I2C_SPI_CHECKER xml file ERROR",
                    "Couldn't open file %s:\n%s." % (filename, file.errorString()))
                return (self.__respondNone)     
        else:           
            return (self.__respondNone)
        xmlReader = QtCore.QXmlStreamReader(file)
        
        if D:
            print("INIT!, devName and Addr")
        regMap=list()       #return values
        deviceName = str() 
        deviceAddr = str()
        while( (not xmlReader.atEnd()) and  (not xmlReader.hasError())):
            xmlReader.readNext() #just skip the intro
            if(xmlReader.isStartDocument()):
                continue
            if(xmlReader.isStartElement()):
                if(xmlReader.name()== 'device'):
                    continue
                elif(xmlReader.name()=='name'):
                    deviceName= self.__readElementData(xmlReader)
                elif(xmlReader.name()=='address'):
                    deviceAddr = self.__readElementData(xmlReader)
                elif(xmlReader.name()=='registers'):
                    continue
                elif(xmlReader.name()=='register'):
                    regMap.append(self.__parseRegister(xmlReader))
                else: 
                    break  #TODO error handler
        if(xmlReader.hasError()):
            QtGui.QMessageBox.critical(self, "I2C_SPI_CHECKER parse xml file ERROR",
                    "Failed string %s." % ( xmlReader.errorString()))
            return (self.__respondNone)
            
        else:    
            if D:
                print("#################LOADING XML FINISHED CORRECTLY#####################")
                print("#################LOADING XML FINISHED CORRECTLY#####################")
                print("DEVICE_NAME %s" %deviceName, "DEVICE_ADDR %s" %deviceAddr)
                print("")
                for i in range( len(regMap)):
                    print("REG_NAME: ", regMap[i][0])
                    print("REG_ADDR: ", regMap[i][1])
                    print("BITMASKS: ")
                    for j in range( len(regMap[i][2])):
                        print("BITMASK: ", regMap[i][2][j])
                    print("REG_ACCESS_ATTRIBUTES: ",regMap[i][3])
                    print("")
        
        xmlReader.clear()   
        return (regMap,deviceName,deviceAddr)

     
    def __parseRegister(self,xmlReader):
        #if D:
        #    print("__parseRegister")
        regParam=() #(str(),str(),str(),list())
        if((not xmlReader.isStartElement())and(xmlReader.name=='register' )):
            return regParam #TODO error handler

        while(not ((xmlReader.isEndElement())and (xmlReader.name()=='register'))):
            xmlReader.readNext()
            if(xmlReader.isStartElement()):
                if(xmlReader.name()=='name'):
                    regParam= regParam+(self.__readElementData(xmlReader),)  #name of the register                
                elif(xmlReader.name()=='address'):
                    regParam= regParam+(self.__readElementData(xmlReader),)  #addr of the register
                elif(xmlReader.name()=='bitmasks'):
                    regParam= regParam+(self.__parseBitmasks(xmlReader),)  #bitmasks of the register
                elif(xmlReader.name()=='byte_access_attr'):
                    regParam= regParam+(self.__parseRegAccessAttr(xmlReader),)  #access parameters of the register
                else:
                    return  regParam #TODO error handler
            
        return  regParam
    
    def __parseBitmasks(self,xmlReader):
        #if D:
        #    print("__parseBitmasks")
        bitmaskList=list() 
        if((not xmlReader.isStartElement())and(xmlReader.name=='bitmasks' )):
            return bitmaskList #TODO error handler
        while(not((xmlReader.isEndElement())and (xmlReader.name()=='bitmasks'))):
            xmlReader.readNext()
            if(xmlReader.isStartElement()):
                if(xmlReader.name()=='bitmask'):
                    bitmaskList.append(self.__parseSingleBitmask(xmlReader))
                else:
                    return  bitmaskList #TODO error handler
        return  bitmaskList
 
    def __parseSingleBitmask(self,xmlReader):
        #if D:
        #    print("__parseSingleBitmask")
        newBitMaskDict={'Name':'' , 'Value':'' , 'Attr':'' } 
        if((not xmlReader.isStartElement())and(xmlReader.name=='bitmask' )):
            return newBitMaskDict #TODO error handler
        while(not ((xmlReader.isEndElement())and (xmlReader.name()=='bitmask'))):
            xmlReader.readNext()
            if(xmlReader.isStartElement()):

                if(xmlReader.name()=='name'):
                    newBitMaskDict['Name']= self.__readElementData(xmlReader) #name of the register
                elif(xmlReader.name()=='mask'):
                    newBitMaskDict['Value']= self.__readElementData(xmlReader)  #addr of the register
                elif(xmlReader.name()=='access_attr'):
                    newBitMaskDict['Attr']= self.__readElementData(xmlReader)
                else:
                    return newBitMaskDict #TODO error handler
        return  newBitMaskDict 
        
    def __parseRegAccessAttr(self,xmlReader): 
        #if D:
        #    print("__parseRegAccessAttr")
        accessAttrList= list()
        if((not xmlReader.isStartElement())and(xmlReader.name=='byte_access_attr' )):
            return accessAttrList #TODO error handler
        while(not ((xmlReader.isEndElement())and (xmlReader.name()=='byte_access_attr'))):
            xmlReader.readNext()
            if(xmlReader.isStartElement()):

                if(xmlReader.name()=='access_attr'):
                    accessAttrList.append(self.__readElementData(xmlReader)) #counted from the LSB 
                else:
                    return accessAttrList #TODO error handler
        return  accessAttrList 
        
        
        
    def __readElementData(self,xmlReader):
        if(not xmlReader.isStartElement()):
            return
        #if D:
        #    print("element Name %s" % xmlReader.name())
        xmlReader.readNext()
        if(not xmlReader.isCharacters()):
            return
        return xmlReader.text()
    
  
    
     
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
   
  
   
    def getModifiedValues(self):
        retValues= {'Name':self.General.bitmaskNameEdit.text(),'Value':self.General.bitmaskValueLabel.text(),'Attr':self.General.accessAttr.text()} 
        return retValues
        

        
class GeneralTab(QtGui.QWidget):
    def __init__(self, regVal, accessAttr,parent=None):
        super(GeneralTab, self).__init__(parent)

        bitmaskNameLabel = QtGui.QLabel("Bitmask Name:")
        self.bitmaskNameEdit = QtGui.QLineEdit()

        bitmaskValLabel = QtGui.QLabel("Bitmask Value")
        self.bitmaskValueLabel = QtGui.QLabel("0x%02x" %(regVal))
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
    
    

