#uszko 21.11.2014


from PySide.QtCore import Qt
from PySide.QtGui import (QDialog, QLabel, QTextEdit, QLineEdit, 
                          QDialogButtonBox, QGridLayout, QVBoxLayout)

class ConnectionDialog(QDialog):

    def __init__(self, parent=None):
        super(ConnectionDialog, self).__init__(parent)

        hostnameLabel = QLabel("Hostname")
        usernameLabel = QLabel("Username")
        passwordLabel = QLabel("Password")
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | 
                                      QDialogButtonBox.Cancel)

        self.hostnameText = QLineEdit()
        self.usernameText = QLineEdit()
        self.passwordText = QLineEdit()

        grid = QGridLayout()
        grid.setColumnStretch(1, 3)
        grid.addWidget(hostnameLabel, 0, 0)
        grid.addWidget(self.hostnameText, 0, 1)
        grid.addWidget(usernameLabel, 1, 0)
        grid.addWidget(self.usernameText, 1, 1)
        grid.addWidget(passwordLabel, 2, 0)#""", Qt.AlignLeft | Qt.AlignTop"""
        grid.addWidget(self.passwordText, 2, 1)  #JUST IN CASE  """, Qt.AlignLeft"""

        layout = QVBoxLayout()
        layout.addLayout(grid)
        layout.addWidget(buttonBox)

        self.setLayout(layout)

        self.setWindowTitle("SSH connection parameters of your Raspberry PI")
        self.setGeometry(300,300,350,150)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    # @property lets us to retrieve data by CreateConnectionDialog.getHostname
    @property
    def getHostname(self):
        return self.hostnameText.text()

    @property
    def getUsername(self):
        return self.usernameText.text()

    @property
    def getPassword(self):
        return self.passwordText.text()

#DEBUG
if __name__ == "__main__":
    import sys
    from PySide.QtGui import QApplication
    
    app = QApplication(sys.argv)

    dialog = ConnectionDialog()
    if (dialog.exec_()):
        hostname = dialog.getHostname
        username = dialog.getUsername
        password = dialog.getPassword
        print("hostname: " + hostname)
        print("username: " + username)
        print("password: " + password)
