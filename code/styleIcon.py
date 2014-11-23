from PySide import QtCore, QtGui



class StyleIcon:

    @staticmethod
    def setStyleAndIcon(widget):
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create("CleanLooks"))
        QtGui.QApplication.setPalette(QtGui.QApplication.palette())
        appIcon=QtGui.QIcon('images/icon.png')
        widget.setWindowIcon(appIcon)
        widget.setWindowTitle("I2C_SPI_CHECKER")