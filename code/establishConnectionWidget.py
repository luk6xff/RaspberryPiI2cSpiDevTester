from PySide.QtCore import (Qt, Signal)
from PySide.QtGui import (QWidget, QLabel, QPushButton, QVBoxLayout)

from createConnectionDialog import ConnectionDialog

class NewConnectionTab(QWidget):
    

    sendSshConnDetails = Signal(str, str, str)

    def __init__(self, parent=None):
        super(NewConnectionTab, self).__init__(parent)

        descriptionLabel = QLabel("You are not connected to Your raspberry PI\n gonna try you ?.")

        continueButton = QPushButton("Continue")
        closeButton = QPushButton("Close")

        layout = QVBoxLayout()
        layout.addWidget(descriptionLabel)
        layout.addWidget(continueButton, 0, Qt.AlignCenter)
        layout.addWidget(closeButton, 1, Qt.AlignCenter)
        self.setLayout(layout)

        continueButton.clicked.connect(self.fireUpConnectionEntry)

    def fireUpConnectionEntry(self):
        conDialog = ConnectionDialog()

        if conDialog.exec_():
            hostname = conDialog.getHostname
            usrname = conDialog.getUsername
            password = conDialog.getUsername
            self.sendSshConnDetails.emit(hostname, usrname, password)


if __name__ == "__main__":

    def printAddress(hostname, usrname, password):
        print("hostname :" + hostname)
        print("usrname: " + usrname)
        print("password: " + password)
    import sys
    from PySide.QtGui import QApplication
    
    app = QApplication(sys.argv)
    newConnTab = NewConnectionTab()
    newConnTab.sendSshConnDetails.connect(printAddress)
    newConnTab.show()
    sys.exit(app.exec_())
