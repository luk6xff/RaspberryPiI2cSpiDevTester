#!/usr/bin/env python
#project uszko, kalicki  19-11-2014

from PySide import QtCore, QtGui
from createConnectionDialog import ConnectionDialog
from establishConnectionWidget import NewConnectionTab
from sshConsole import SshConsole
from sshconnection import SshConnection
from messageBoxWrapper import MessageBox
from styleIcon import StyleIcon

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        StyleIcon.setStyleAndIcon(self)
        self.sshClient=None
        self.console= None

        self.setWindowTitle("I2C_SPI_CHECKER")
        self.setGeometry(500,500,500,500)

    def newDevice(self):
        return


    def sshConnectionSetup(self):
        self.newConnTab = NewConnectionTab()
        self.newConnTab.sendSshConnDetails.connect(self.sshMakeConnection)
        self.newConnTab.show()
        return
    
    def sshMakeConnection(self,hostname, username, password):   # here we get ssh parameters for our connection to raspberry
        conDialog = ConnectionDialog()
        self.hostname = hostname
        self.username = username
        self.password = password
        print("hostname: " + self.hostname)
        print("usrname: " + self.username)
        print("password: " + self.password)
        print('paramiko connection starts')
        self.sshClient= SshConnection(self.hostname, self.username,self.password )
        #self.sshClient= SshConnection('172.16.1.102','pi', 'raspberry')  #for tests 
        self.sshClient.connect() #try to connect to raspberry
        return
    
    def displayConsole(self):
        if(self.sshClient is None):
            MessageBox.warningMessage("You're not connected to RPi, Do it first and then open console","OK",None,None)
            return
        if (self.console is None):
            self.console = SshConsole(self.sshClient)
            print('Console init')
            self.console.exec_()
            self.console =None
        else:
            print('Console is already being displayed!')
        return

    def save(self):
        filename, filtr = QtGui.QFileDialog.getSaveFileName(self,
                "Choose a file name", '.', "rd (*.rd)")
        if not filename:
            return

        file = QtCore.QFile(filename)
        if not file.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, "I2C_SPI_CHECKER",
                    "Cannot write file %s:\n%s." % (filename, file.errorString()))
            return

        out = QtCore.QTextStream(file)
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        out << self.textEdit.toHtml()
        QtGui.QApplication.restoreOverrideCursor()

        self.statusBar().showMessage("Saved '%s'" % filename, 2000)

    def undo(self):
        document = self.textEdit.document()
        document.undo()


    def about(self):
        QtGui.QMessageBox.about(self, "About I2C_SPI_CHECKER",
                "project uszko kalicki")

    def setIcon(self):
        appIcon=QtGui.QIcon('images/icon.png')
        self.setWindowIcon(appIcon)

    def createActions(self):

        self.createConnection = QtGui.QAction(QtGui.QIcon('images/connection.png'),
                "&Create SSH connection", self, shortcut=QtGui.QKeySequence.New,
                statusTip="Create SSH connection to your Raspberry PI : ] ",
                triggered=self.sshConnectionSetup)

        self.newDeviceAct = QtGui.QAction(QtGui.QIcon('images/newDevice.png'),
                "&Add New Device", self, shortcut=QtGui.QKeySequence.New,
                statusTip="Create a new form of registers of a new device",
                triggered=self.newDevice)

        self.saveAct = QtGui.QAction(QtGui.QIcon('images/save.png'),
                "&Save...", self, shortcut=QtGui.QKeySequence.Save,
                statusTip="Save the new added device",
                triggered=self.save)

        self.undoAct = QtGui.QAction(QtGui.QIcon('images/undo.png'),
                "&Undo", self, shortcut=QtGui.QKeySequence.Undo,
                statusTip="Undo the last editing action", triggered=self.undo)

        self.consoleAct = QtGui.QAction(QtGui.QIcon('images/console.png'),
                "&Console SSH", self, shortcut=QtGui.QKeySequence.MoveToStartOfLine,    #button "HOME" on your keyboard
                statusTip="Display SSH Console", triggered=self.displayConsole)

        self.quitAct = QtGui.QAction("&Quit", self, shortcut="Ctrl+Q",
                statusTip="Quit the application", triggered=self.close)

        self.aboutAct = QtGui.QAction("&About the project", self,
                statusTip="Show the application's About box",
                triggered=self.about)

        self.aboutQtAct = QtGui.QAction("About &Qt", self,
                statusTip="Show the Qt library's About box",
                triggered=QtGui.qApp.aboutQt)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newDeviceAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.quitAct)

        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.undoAct)

        self.viewMenu = self.menuBar().addMenu("&View")

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

    def createToolBars(self):
        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.addAction(self.createConnection)
        self.fileToolBar.addAction(self.newDeviceAct)
        self.fileToolBar.addAction(self.saveAct)
        self.fileToolBar.addAction(self.consoleAct)
        self.editToolBar = self.addToolBar("Edit")
        self.editToolBar.addAction(self.undoAct)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")



if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())

