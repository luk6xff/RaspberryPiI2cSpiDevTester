
from PySide import QtCore, QtGui
from registersFormUi import Ui_RegitersForm
from styleIcon import StyleIcon



class DeviceDescriptionSheet(QtGui.QWidget):
  def __init__(self, parent=None):
    super(DeviceDescriptionSheet, self).__init__(parent)
    self.ui =  Ui_RegitersForm()
    self.ui.setupUi(self)
    StyleIcon.setStyleAndIcon(self)
   

 
 
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    myDevice = DeviceDescriptionSheet()
    myDevice.show()
    sys.exit(app.exec_())