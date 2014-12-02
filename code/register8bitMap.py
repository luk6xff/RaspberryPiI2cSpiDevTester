#uszko 26.11.2014
from PySide import QtCore, QtGui
from enum import Enum

D = False    #debug enebled

class Reg8BitMap(QtGui.QWidget):
    NumOfBits = 8
    regValueChanged = QtCore.Signal(int)
    regAccessPermissionChanged= QtCore.Signal(list)
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
                RectRenderArea(rectPath)]  #1 byte
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
            if(self.renderBitsArea[Reg8BitMap.NumOfBits-i-1].getWriteReadAttribute()==WriteReadBitPrivilege.NA):
                self.byteRegVal&= ~(1<<i)
            if(self.renderBitsArea[Reg8BitMap.NumOfBits-i-1].getFieldState()==BitState.Blocked):
                self.byteRegVal&= ~(1<<i)
            elif(self.renderBitsArea[Reg8BitMap.NumOfBits-i-1].getFieldState()==BitState.Pressed):
                self.byteRegVal|= 1<<i
            else:
                self.byteRegVal&= ~(1<<i)       
        self.regValueChanged.emit(self.byteRegVal)
        if D:
            print("REG_VAL = %d" % self.byteRegVal)
    
    def updateRegAccesPermissionParam(self):
        self.byteRegAccessList=list();
        for i in range(Reg8BitMap.NumOfBits):
            self.byteRegAccessList.append(self.renderBitsArea[Reg8BitMap.NumOfBits-i-1].getWriteReadAttribute().value) ##TODO
        if D:
            print(self.byteRegAccessList)         
        self.regAccessPermissionChanged.emit(self.byteRegAccessList)
        
    def bitMaskCreated(self, bitmask): ######## invoked after creation of bitmask 
        for i in range(Reg8BitMap.NumOfBits):
            if(bitmask & (1<<i)):
                self.renderBitsArea[Reg8BitMap.NumOfBits-i-1].bitState= BitState.Blocked
                self.renderBitsArea[Reg8BitMap.NumOfBits-i-1].setFieldState()
        self.updateRegisterValue()
        
    def bitMaskDestroyed(self, bitmask): ########
        for i in range(Reg8BitMap.NumOfBits):
            if(bitmask & (1<<i)):
                self.renderBitsArea[Reg8BitMap.NumOfBits-i-1].bitState= BitState.Pressed #pressed cuz then setFieldState() will update it to not pressed automatically
                self.renderBitsArea[Reg8BitMap.NumOfBits-i-1].setFieldState()
        self.updateRegisterValue()
    
    def setConnections(self):
        for i in range(Reg8BitMap.NumOfBits):
            self.renderBitsArea[i].bitValueChanged.connect(self.updateRegisterValue)
            self.renderBitsArea[i].bitAccessPermissionChanged.connect(self.updateRegAccesPermissionParam)
        
    def fillGradientChanged(self):
        for i in range(Reg8BitMap.NumOfBits):
            self.renderBitsArea[i].setFillGradient(RectRenderArea.ColorBitInactive[0],RectRenderArea.ColorBitInactive[1])

    def penColorChanged(self):
        for i in range(Reg8BitMap.NumOfBits):
            self.renderBitsArea[i].setPenColor(QtCore.Qt.blue)

    def __del__(self):
        self.renderBitsArea = None    

 


 
class BitState(Enum):
    NotPressed = 0
    Pressed =1
    Blocked =2   #when Bitmask has been created we cannot modify it further
    
class WriteReadBitPrivilege(Enum):
    NA="N/A"
    Write=" W "
    Read=" R "
    WriteRead="R/W"
    

    
class RectRenderArea(QtGui.QWidget):
    ColorBitActive= [QtCore.Qt.white,QtCore.Qt.green]
    ColorBitInactive= [QtCore.Qt.white,QtCore.Qt.red]
    ColorBitNotUsed= [QtCore.Qt.white,QtCore.Qt.cyan]
    ColorBitBlocked= [QtCore.Qt.white,QtCore.Qt.yellow]
    bitValueChanged = QtCore.Signal()
    bitAccessPermissionChanged= QtCore.Signal()
    def __init__(self, path, parent=None):
        super(RectRenderArea, self).__init__(parent)

        self.path = path
        self.penWidth = 1
        self.setBackgroundRole(QtGui.QPalette.Base)
        self.bitState = BitState.NotPressed
        self.setWriteReadAttribute(WriteReadBitPrivilege.WriteRead)
    
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
        if(self.bitState is BitState.Blocked):   #when bit blocked
           self.setFillGradient(RectRenderArea.ColorBitBlocked[0],RectRenderArea.ColorBitBlocked[1]) 
           
        elif(self.getWriteReadAttribute() is not WriteReadBitPrivilege.NA):
            if(self.bitState is BitState.NotPressed):
                    self.bitState = BitState.Pressed
                    self.setFillGradient(RectRenderArea.ColorBitActive[0],RectRenderArea.ColorBitActive[1])
            else:
                self.bitState = BitState.NotPressed
                self.setFillGradient(RectRenderArea.ColorBitInactive[0],RectRenderArea.ColorBitInactive[1])
        else: 
            self.bitState = BitState.NotPressed
        #self.update() update is being done in setFillGradient method
        
    def getFieldState(self):
        return self.bitState 
        
    def setWriteReadAttribute(self,attr):
        self.writeReadAttribute= attr
        if(self.getWriteReadAttribute() is WriteReadBitPrivilege.NA):
           self.setFillGradient(RectRenderArea.ColorBitNotUsed[0], RectRenderArea.ColorBitNotUsed[1])
        else:
            self.setFillGradient(RectRenderArea.ColorBitInactive[0],RectRenderArea.ColorBitInactive[1])
        #self.update() update is being done in setFillGradient method
    
    def getWriteReadAttribute(self):
        return self.writeReadAttribute 
        

            
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.scale(0.6, 0.9)   # i really don't get it HOW IT WORKS!! but those values seem to handle it quite well
        if D:
            print("%d" %self.height() , "%d" %self.width())
        
        painter.setPen(QtGui.QPen(self.penColor, self.penWidth,
                QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
        gradient = QtGui.QLinearGradient(0, 0, 0, 100)
        gradient.setColorAt(0.0, self.fillColor1)
        gradient.setColorAt(1.0, self.fillColor2)
        painter.setBrush(QtGui.QBrush(gradient))
        painter.setRenderHint(QtGui.QPainter.Antialiasing);
        font =QtGui.QFont("Helvetica")
        font.setPointSize(12);
        painter.setFont(font);
        #self.path.addText(30,45,font, "R/W")
        if D:
            print("PAINTING...")
        painter.drawPath(self.path)
        painter.drawText(25,45, str(self.writeReadAttribute.value));
        if D:
            print("%s" % str(self.writeReadAttribute.name))
        
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            if D:
                print("X=%f" %event.x(), "Y=%f"%event.y())
            self.setFieldState()
            self.bitValueChanged.emit()  #signal for Register window to check the value
            self.update()
        elif event.button() == QtCore.Qt.RightButton:
            if(self.bitState is BitState.Blocked):     #just do nothing here , bit is blocked
                return
            flag= 0    
            for params in WriteReadBitPrivilege:
                if flag==1:
                    self.setWriteReadAttribute(params)
                    break
                if params == self.getWriteReadAttribute():
                    if params == WriteReadBitPrivilege.WriteRead:
                        self.setWriteReadAttribute(WriteReadBitPrivilege.NA)
                        break
                    flag =1
            self.bitState = BitState.Pressed #just to cheat the widget a little LOL
            self.setFieldState()
            self.bitValueChanged.emit()  #signal for Register window to check the value        
            self.bitAccessPermissionChanged.emit()  #signal for Register window to check the value
            self.update()
        else:
            super(RectRenderArea, self).mousePressEvent(event)  



if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    reg8bit = Reg8BitMap()
    reg8bit.show()
    sys.exit(app.exec_())
