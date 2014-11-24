#ui tests
from PySide import QtCore, QtGui, QtUiTools

class RegistersForm(QtGui.QWidget):
    def __init__(self, parent=None):
        super(RegistersForm, self).__init__(parent)
        loader = QtUiTools.QUiLoader()
        file = QtCore.QFile("uiRegisterForm.ui")
        file.open(QtCore.QFile.ReadOnly)
        myWidget = loader.load(file, self)
        file.close()

        layout = QtGui.QVBoxLayout()
        layout.addWidget(myWidget)
        self.setLayout(layout)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = RegistersForm()
    MainWindow.show()
    sys.exit(app.exec_())      