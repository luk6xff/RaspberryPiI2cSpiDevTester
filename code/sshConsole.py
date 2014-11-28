#uszko 23-11-2014

#pyside-uic uiRegisterForm.ui -o reigersFormUi.py

from PySide import QtCore, QtGui
from sshconnection import SshConnection
from styleIcon import StyleIcon
class SshConsole(QtGui.QDialog):

    def __init__(self,sshClient):
        super(SshConsole, self).__init__()
        self.sshClient=sshClient 
        self.createMenu()
        self.createSettingsButtonsGroupBox()
        self.createCommandGroupBox()
        self.createResponseTextEdit()
        self.createDialogButtons()
        self.initConnections()

        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.setMenuBar(self.menuBar)
        mainLayout.addWidget(self.settingsGroupBox)
        mainLayout.addWidget(self.commandGroupBox)
        mainLayout.addWidget(self.responseGroupBox)
        mainLayout.addWidget(self.dialogButtonBox)
        self.setLayout(mainLayout)
        StyleIcon.setStyleAndIcon(self)
        self.setWindowTitle("SSH CONSOLE")

    def createMenu(self):
        self.menuBar = QtGui.QMenuBar()

        self.fileMenu = QtGui.QMenu("&File", self)
        self.exitAction = self.fileMenu.addAction("E&xit")
        self.menuBar.addMenu(self.fileMenu)

        self.exitAction.triggered.connect(self.accept)

    def createSettingsButtonsGroupBox(self):
        self.settingsGroupBox = QtGui.QGroupBox("Settings")
        layout = QtGui.QHBoxLayout()
        self.clearConsoleButton = QtGui.QPushButton("Clear")
        layout.addWidget(self.clearConsoleButton)
        for i in range(3):
            button = QtGui.QPushButton("Empty %d" % (i + 1))
            layout.addWidget(button)

        self.settingsGroupBox.setLayout(layout)

    def createCommandGroupBox(self):
        self.commandGroupBox = QtGui.QGroupBox("Command")
        layout = QtGui.QFormLayout()
        self.command= QtGui.QLineEdit()
        layout.addRow(QtGui.QLabel("->"), self.command)
        self.commandGroupBox.setLayout(layout)

    def createResponseTextEdit(self):
        self.responseGroupBox = QtGui.QGroupBox("Data received from Raspberry PI")
        self.response = QtGui.QTextEdit()
        layout = QtGui.QFormLayout()
        layout.addWidget(self.response)
        self.responseGroupBox.setLayout(layout)
        self.cursor = self.response.textCursor()
        self.cursor.movePosition(QtGui.QTextCursor.Start)


    def createDialogButtons(self):
        self.sendButton = QtGui.QPushButton("&Send")
        self.cancelButton = QtGui.QPushButton("&Cancel")
        self.dialogButtonBox = QtGui.QDialogButtonBox()
        self.dialogButtonBox.addButton(self.sendButton,QtGui.QDialogButtonBox.ActionRole)
        self.dialogButtonBox.addButton(self.cancelButton,QtGui.QDialogButtonBox.ActionRole)

    def initConnections(self):
        self.clearConsoleButton.clicked.connect(self.response.clear)
        self.cancelButton.clicked.connect(self.reject)
        self.sendButton.clicked.connect(self.executeCommand)
    

    def executeCommand(self):
        #response = self.sshClient.executeCommand(self.command.text())
        response = self.sshClient.executeCommand(self.command.text(),True)
        #self.addText(response['STDOUT']+'\n'+response['STDERR']+'\n'+response['RET_VAL']+'\n')
        print("COMMAND HAS BEEN EXECUTED")
        #if (response is not None):
        #    print(response)                                   TODO !!!!!!
        for line in response['STDOUT']:
            print (line.strip('\n'))
            self.addText(line.strip('\n')+'\n')
        self.addText('\n')
    
    def addText(self,text):
        
        self.cursor.beginEditBlock()
        self.cursor.movePosition(QtGui.QTextCursor.Down,
                QtGui.QTextCursor.MoveAnchor, 2)
        self.cursor.insertText(text)
        self.cursor.endEditBlock()
        #self.response.setPlainText(text)

#debug
if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    sshClient= SshConnection('172.16.1.102', 22, 'pi', 'raspberry')  #for tests 
    sshClient.connect() #try to connect to raspberry
    console = SshConsole(sshClient)
    console.addText("AAAAAA")
    console.addText("AAAAAA")
    sys.exit(console.exec_())
