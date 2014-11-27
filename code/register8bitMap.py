from PySide import QtCore, QtGui
from enum import Enum


class Reg8BitMap(QtGui.QWidget):
    NumOfBits = 8
    regValueChanged = QtCore.Signal(int)
    def __init__(self, parent =None):
        super(Reg8BitMap,self).__init__(parent)
        
        
        rectPath = QtGui.QPainterPath()
        rectPath.moveTo(10.0, 20.0)
        rectPath.lineTo(70.0, 20.0)
        rectPath.lineTo(70.0, 60.0)
        rectPath.lineTo(10.0, 60.0)
        rectPath.closeSubpath()
        self.renderBitsArea = [RectRenderArea(rectPath), 
                RectRenderArea(rectPath),
                RectRenderArea(rectPath), 
                RectRenderArea(rectPath),
                RectRenderArea(rectPath), 
                RectRenderArea(rectPath),
                RectRenderArea(rectPath), 
                RectRenderArea(rectPath)]
        assert len(self.renderBitsArea) == Reg8BitMap.NumOfBits

        mainLayout = QtGui.QGridLayout()
        mainLayout.setHorizontalSpacing(1)
        for i in range(Reg8BitMap.NumOfBits):
            mainLayout.addWidget(self.renderBitsArea[i], 0 , i)
        self.setLayout(mainLayout)
        
        self.byteRegVal =0
        self.setConnections()
        self.fillGradientChanged()
        self.penColorChanged()
        self.setWindowTitle("I2C_SPI_CHECKER")
        
    def updateRegisterValue(self):
        self.byteRegVal=0;
        for i in range(Reg8BitMap.NumOfBits):
            if(self.renderBitsArea[Reg8BitMap.NumOfBits-i-1].getFieldState()==BitState.Pressed):
                self.byteRegVal|= 1<<i
            else:
                self.byteRegVal&= ~(1<<i)       
        self.regValueChanged.emit(self.byteRegVal)
        print("REG_VAL = %d" % self.byteRegVal)
    
    def setConnections(self):
        for i in range(Reg8BitMap.NumOfBits):
            self.renderBitsArea[i].bitValueChanged.connect(self.updateRegisterValue)
        
    def fillGradientChanged(self):
        for i in range(Reg8BitMap.NumOfBits):
            self.renderBitsArea[i].setFillGradient(RectRenderArea.ColorBitInactive[0],RectRenderArea.ColorBitInactive[1])

    def penColorChanged(self):
        for i in range(Reg8BitMap.NumOfBits):
            self.renderBitsArea[i].setPenColor(QtCore.Qt.blue)

    def __del__(self):
        self.renderBitsArea = None    

 


 
class BitState(Enum):
    NotPressed = 0,
    Pressed =1
    

    

    
class RectRenderArea(QtGui.QWidget):
    ColorBitActive= [QtCore.Qt.white,QtCore.Qt.green]
    ColorBitInactive= [QtCore.Qt.white,QtCore.Qt.red]
    bitValueChanged = QtCore.Signal()
    def __init__(self, path, parent=None):
        super(RectRenderArea, self).__init__(parent)

        self.path = path
        self.bitState = BitState.NotPressed
        self.penWidth = 1
        self.rotationAngle = 0
        self.setBackgroundRole(QtGui.QPalette.Base)
    
    
    def minimumSizeHint(self):
        return QtCore.QSize(30, 30)

    def sizeHint(self):
        return QtCore.QSize(60, 60)

    def setFillRule(self, rule):
        self.path.setFillRule(rule)
        self.update()

    def setFillGradient(self, color1, color2):
        self.fillColor1 = color1
        self.fillColor2 = color2
        self.update()

    def setPenWidth(self, width):
        self.penWidth = width
        self.update()

    def setPenColor(self, color):
        self.penColor = color
        self.update()

    def setFieldState(self):
        if(self.bitState is BitState.NotPressed): 
            self.bitState = BitState.Pressed
            self.setFillGradient(RectRenderArea.ColorBitActive[0],RectRenderArea.ColorBitActive[1])
        else:
            self.bitState = BitState.NotPressed
            self.setFillGradient(RectRenderArea.ColorBitInactive[0],RectRenderArea.ColorBitInactive[1])
    
    def getFieldState(self):
        return self.bitState 
            
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.scale(0.6, 0.9)   # i really don't get it but those values work most properly
        print("%d" %self.height() , "%d" %self.width())
        
        painter.setPen(QtGui.QPen(self.penColor, self.penWidth,
                QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
        gradient = QtGui.QLinearGradient(0, 0, 0, 100)
        gradient.setColorAt(0.0, self.fillColor1)
        gradient.setColorAt(1.0, self.fillColor2)
        painter.setBrush(QtGui.QBrush(gradient))
        painter.drawPath(self.path)
        
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            print("X=%f" %event.x(), "Y=%f"%event.y())
            self.setFieldState()
            self.bitValueChanged.emit()  #signal for Register window to check the value
            self.update()
        else:
            super(RectRenderArea, self).mousePressEvent(event)  



if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    reg8bit = Reg8BitMap()
    reg8bit.show()
    sys.exit(app.exec_())
