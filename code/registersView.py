from PySide import QtCore, QtGui
from registersViewUi import Ui_RegistersView
from sshconnection import SshConnection
from threading import Thread
from time import sleep
import sys
import re
import ast

D=True #debug enabled

#C:\Python34\Scripts\pyside-uic.exe uiRegistersView.ui -o registersViewUi.py

class RegistersViewer(QtGui.QWidget):

    def __init__(self,  sshClient,deviceAddress,deviceName,regs,parent=None):
        self.deviceAddress = deviceAddress;
        self.sshClient=sshClient 
        super(RegistersViewer, self).__init__(parent)
        
        self.ui =  Ui_RegistersView()
        self.ui.setupUi(self)
        self.registersList= list();  #sth aka MVC dessign pattern, all stuff is stored in one main list
        self.formulasList = list();
        
        self.initConnections()
        
        
        self.maxRegisterNumber=0;
        self.minRegisterNumber=9999;
        self.loadRegisters(regs)
        
        
    def initConnections(self):			# setup all connections of signal and slots
        self.ui.AddFormulaButton.clicked.connect(self.addFormulaClicked);
    
    def readDeviceInformations(self):	#read all registers information from XML file
        i=2;
        # dont do anything
    
    def addNewRegister(self,number, name, value, function):
        self.ui.RegistersTable.insertRow(self.ui.RegistersTable.rowCount());
        #"0x%02x" % value
        regTuple=(QtGui.QTableWidgetItem(("0x%02x" % number)),QtGui.QTableWidgetItem(("%s" % name)),QtGui.QTableWidgetItem(( value)),QtGui.QTableWidgetItem(("%s" % function)));
        self.registersList.append(regTuple);
        
        self.ui.RegistersTable.setItem(self.ui.RegistersTable.rowCount()-1,0,self.registersList[-1][0]);
        self.ui.RegistersTable.setItem(self.ui.RegistersTable.rowCount()-1,1,self.registersList[-1][1]);
        self.ui.RegistersTable.setItem(self.ui.RegistersTable.rowCount()-1,2,self.registersList[-1][2]);
        self.ui.RegistersTable.setItem(self.ui.RegistersTable.rowCount()-1,3,self.registersList[-1][3]);
        
        if number<self.minRegisterNumber:
            self.minRegisterNumber=number;
        if number>self.maxRegisterNumber:
            self.maxRegisterNumber=number;
        
        #TODO add protection befor adding the same register number or name twice.
    
    def loadRegisters(self,regList):
        if regList is None:
            return
        for i in range(len(regList)):
            self.addNewRegister(i,regList[i][0],regList[i][1],'none')
            
        
    
    
    
    def updateRegisterValue(self,number,value):
        for i in range(0,self.ui.RegistersTable.rowCount()):    #look for register with "number"
            if(self.ui.RegistersTable.item(i,0).text())==("0x%02x" % number):      #check number match
                self.ui.RegistersTable.setItem(i,2,QtGui.QTableWidgetItem(("0x%02x" % value)));
                break;
    
    def getRegisterValue(self,number):
        for i in range(0,self.ui.RegistersTable.rowCount()):        #look for register with "number"
           if (self.ui.RegistersTable.item(i,0).text())==("0x%02x" % number):		#check number match
                return int(self.ui.RegistersTable.item(i,2).text(),16);
        return 0;
    
    def updateRegisterFunction(self,number):	#this function updates automaticly function column based on the register value
        i=2;
    
    def RPiReadRegisters(self):
        while 1:
            startIndex=self.minRegisterNumber;
            stopIndex=self.maxRegisterNumber+1;
            
            command = "python i2c_program/i2c_com.py read_block "+("0x%02x" % self.deviceAddress)+" "+("%d" % startIndex)+" "+("%d" % stopIndex);
            
            response = self.sshClient.executeCommand(command,True)
            for line in response['STDOUT']:
                #print (line.strip('\n'))
                readValues = ast.literal_eval(line.strip('\n'))
            for i_reg in range(0,stopIndex-startIndex):
                self.updateRegisterValue(i_reg+startIndex,readValues[i_reg]);
            #sleep(0.2);
    
            self.updateFormulas();

    def RpiSetRegister(self,register,value):
        command = "python i2c_program/i2c_com.py set_reg "+("0x%02x" % self.deviceAddress)+" "+("0x%02x"  % reg)+" "+("0x%02x" % value);
        
    def addFormulaClicked(self):
        print ("AddFormula()");
        formulaText = self.ui.FormulaText.toPlainText();
        
        reFormName = re.compile('\[(.*?)\]');
        reFormNameResult = reFormName.search(formulaText);
        if reFormNameResult:
            name=(reFormNameResult.group(0))[1:-1];
        else:
            return;
        
        formulaEval = formulaText.replace("["+name+"]","");
        print (formulaEval);
        self.addFormula(name,formulaEval);
    
    def addFormula(self,name,formula):
    
        formulaEval = formula;
        
        self.ui.FormulasTable.insertRow(self.ui.FormulasTable.rowCount());
        
        value=0;
        formulaTuple=(QtGui.QTableWidgetItem(("%s" % name)),QtGui.QTableWidgetItem(("0")), QtGui.QTableWidgetItem(("%s" % formulaEval)));
        self.formulasList.append(formulaTuple);
        
        self.ui.FormulasTable.setItem(self.ui.FormulasTable.rowCount()-1,0,self.formulasList[-1][0]);
        self.ui.FormulasTable.setItem(self.ui.FormulasTable.rowCount()-1,1,self.formulasList[-1][1]);
        self.ui.FormulasTable.setItem(self.ui.FormulasTable.rowCount()-1,2,self.formulasList[-1][2]);
        
    
    def setFormulaValue(self,number,value):
        self.ui.FormulasTable.setItem(number,1,QtGui.QTableWidgetItem(("%s" % value)));
    
    def updateFormulas(self):
        for i in range(0,len(self.formulasList)):
            evalCommand = self.formulasList[i][2].text();
            reFindR = re.compile('[r][0-9]+');
            reFindRResult = reFindR.findall(evalCommand);
            if reFindRResult:
                for ii in range(0,len(reFindRResult)):
                    regNumber = int((re.findall('\d+',reFindRResult[ii]))[0]);
                    evalCommand = evalCommand.replace(reFindRResult[ii],'self.getRegisterValue('+("%s"%regNumber)+')');
            evalRet=(eval(evalCommand));
            self.setFormulaValue(i,evalRet);

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    
    
    sshClient=SshConnection('172.16.1.102','pi', 'raspberry');
    sshClient.connect();
    
    myDeviceRegisters = RegistersViewer(sshClient,0x4D,'ADXL345',None);
    myDeviceRegisters.show();
    
    myDeviceRegisters.addNewRegister(0,"DataH",0x12,"ADC high value");
    myDeviceRegisters.addNewRegister(1,"DataL",0x10,"ADC low value");
    #myDeviceRegisters.addNewRegister(3,"Reg3",0x10,"This register doesnt do anything");
    
    myDeviceRegisters.addFormula("ADC data"," r0*256+r1");
    
    update_thread = Thread(target=myDeviceRegisters.RPiReadRegisters) 
    update_thread.daemon = True
    update_thread.start()
    

    sys.exit(app.exec_())
    
    
    



    