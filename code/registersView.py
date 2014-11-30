from PySide import QtCore, QtGui
from registersViewUi import Ui_RegistersView
from threading import Thread
from time import sleep
import sys
import re

D=True #debug enabled

class RegistersViewer(QtGui.QWidget):

	def __init__(self, parent=None):
		super(RegistersViewer, self).__init__(parent)
		self.ui =  Ui_RegistersView()
		self.ui.setupUi(self)
		self.registersList= list()  #sth aka MVC dessign pattern, all stuff is stored in one main list
		self.setItems()
		self.initConnections()
		if D:
			self.debugCounter = 0;
		#StyleIcon.setStyleAndIcon(self)
	
	def setItems(self):
		i=2;
		# dont do anything
	
	def initConnections(self):			# setup all connections of signal and slots
		i=2;
		# dont do anything
	
	def readDeviceInformations(self):	#read all registers information from XML file
		i=2;
		# dont do anything
	
	def addNewRegister(self,number, name, value, function):
		self.ui.RegistersTable.insertRow(self.ui.RegistersTable.rowCount());
		
		regTuple=(QtGui.QTableWidgetItem(("0x%02x" % number)),QtGui.QTableWidgetItem(("%s" % name)),QtGui.QTableWidgetItem(("0x%02x" % value)),QtGui.QTableWidgetItem(("%s" % function)));
		self.registersList.append(regTuple);
		
		self.ui.RegistersTable.setItem(self.ui.RegistersTable.rowCount()-1,0,self.registersList[-1][0]);
		self.ui.RegistersTable.setItem(self.ui.RegistersTable.rowCount()-1,1,self.registersList[-1][1]);
		self.ui.RegistersTable.setItem(self.ui.RegistersTable.rowCount()-1,2,self.registersList[-1][2]);
		self.ui.RegistersTable.setItem(self.ui.RegistersTable.rowCount()-1,3,self.registersList[-1][3]);
		
		#TODO add protection befor adding the same register number or name twice.
	
	def updateRegisterValue(self,number,value):
		for i in range(0,self.ui.RegistersTable.rowCount()):	#look for register with "number"
			if (self.ui.RegistersTable.itemAt(i,0).text())==("0x%02x" % number):		#check number match
				self.ui.RegistersTable.setItem(i,2,QtGui.QTableWidgetItem(("0x%02x" % value)));
				print ("Matched");
				break;
	
	def updateRegisterFunction(self,number):	#this function updates automaticly function column based on the register value
		i=2;
	
	def readRegisterFromTheDevice(self):
		while 1:
			self.updateRegisterValue(0x01,self.debugCounter);
			self.debugCounter=self.debugCounter+1;
			print (self.debugCounter);
			sleep(1);


if __name__ == "__main__":
	import sys
	app = QtGui.QApplication(sys.argv)
	myDeviceRegisters = RegistersViewer();
	myDeviceRegisters.addNewRegister(1,"Reg1",0x12,"This register doesnt do anything");
	myDeviceRegisters.show();
	
	update_thread = Thread(target=myDeviceRegisters.readRegisterFromTheDevice) 
	update_thread.daemon = True
	update_thread.start()
	
	sys.exit(app.exec_())
    