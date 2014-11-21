#import connect
from PySide import QtCore, QtGui

class Window(QtGui.QWidget):

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        windowWidth = 550
        windowHeight = 350

        self.establishedConnection = ""

        connectButton = self.createButton("&Connect", self.conn)
        disconnectButton = self.createButton("&Disconnect", self.disconnect)
        grid = QtGui.QGridLayout()
        grid.addWidget(connectButton, 3, 3)
        grid.addWidget(disconnectButton, 4, 3)
        #grid.addWidget(self.createList(), 1, 0, 1, 4)

        self.setLayout(grid)     

        self.resize(windowWidth, windowHeight)
        self.setWindowTitle("FTP Program")

    def conn(self):
        connection = 1#connect.Connection()
        self.establishedConnection = connection

    def disconnect(self):
        self.establishedConnection.disconnect()

    def createButton(self, text, member):
        button = QtGui.QPushButton(text)
        button.clicked.connect(member)
        return button

if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    gui = Window()
    gui.show()
    sys.exit(app.exec_())