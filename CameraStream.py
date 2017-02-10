#!/usr/bin/python
 
import sys
import cv2
from PySide.QtGui import QImage, QIcon, QPainter, QWidget, QApplication, QMainWindow, QLabel, QLineEdit, \
QHBoxLayout, QVBoxLayout
from PySide.QtCore import QTimer, QObject, QThread 
import qimage2ndarray  

class CameraStream(QWidget,QObject) :  
    _image = QImage("../myName.jpg")
    _terminate = False
    _timer = QTimer()  
    def __init__(self,parent=None) :
        super(CameraStream,self).__init__(parent)
        self.setUi()
    
    def setUi(self) : 
        self.setGeometry(300,300,300,220) 
        self.setWindowTitle('Camera Stream')
        self.camera = cv2.VideoCapture(0)

        if self.camera.isOpened() :
            print "camera is open, ready to stream" 
        else : 
            print "cant open the camera!"
            exit  
        self._timer.timeout.connect(self.grabFeed)
        self._timer.start(30)  

    def paintEvent(self,e) :
        self.painter = QPainter(self)   
        self.painter.drawImage(e.rect(),self._image)
        self.painter.end()

    def grabFeed(self) :  
        ret,frame = self.camera.read()
        if ret :  
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # grayImage 
            self._image = qimage2ndarray.array2qimage(gray)
            self.repaint() # post a paint event

    def __del__(self) : 
        self.camera.release()  
    def freeze(self) : 
        self._timer.disconnect(self)
    def start(self) :
        self._timer.timeout.connect(self.grabFeed)
        self._timer.start(30)
if __name__ == '__main__' : 
    app = QApplication(sys.argv)
    cameraStream = CameraStream() 
    cameraStream.move(100,100)
    cameraStream.resize(600,500)
    cameraStream.show()
    sys.exit(app.exec_())