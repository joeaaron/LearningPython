from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtCore import Qt, QByteArray, QString, QEvent
from PyQt4.QtNetwork import *  
from PyQt4.QtGui import QMessageBox, QInputDialog, QPlainTextEdit, QPalette, QTextCursor, QKeyEvent, QFileDialog
import sys, pickle

from component import *
RECT = [(-0.5, 0.35, 0.5, 0.35), (-0.5, 0.35, 0.5, 0.35), # small pan
        (-0.5, -0.5, -0.5, 0.5), (-0.5, -0.5, -0.5, 0.5),
        (0.23, -0.5, 0.23, 0.5), (0.23, -0.5, 0.23, 0.5),
        (0.4, 0, 0, 0.4), (-0.65, 0, -0.2, 0.45),
        (-1, 1.45, 1, 1.45),   # big pan
        (-1.45, -1, -1.45, 1),
        (1.45, -1, 1.45, 1),
        (1.8, 0, 0, 1.8), (-1.8, 0, -0.2, 1.8),
        ]
ROTATE=[0, 0, 90, 90, 90, 90, 0, 0,      0, 90, 0, 0, 0]
VIEW=[1, 1, 2, 2, 3, 3, 4, 4,     5, 6, 7, 8, 9]
class QCheck(QtGui.QDialog):
    def __init__(self, parent = None, lasers = None ):
        super(QCheck, self).__init__()   
        self.ui = uic.loadUi('ui/check.ui', self)
        if not lasers:
            self.lasers = pickle.load( open("image\\check.dat", "rb"))
        else:
            self.lasers = lasers
        for i in range(0, len(self.lasers)):
            view = self.ui.__dict__['graphicsView_%d'%(VIEW[i])]
            
            rect = RECT[i]
            if not view.scan or i in [7]:
                f = lambda x: x / view.resolution
                line = view.scene.addLine(f(rect[0]),f(rect[1]), f(rect[2]), f(rect[3]))
                pen = QtGui.QPen(Qt.gray)
                pen.setWidth(10);
                line.setPen(pen)
                
            x1 = min(rect[0], rect[2])
            x2 = max(rect[0], rect[2])
            y1 = min(rect[1], rect[3])
            y2 = max(rect[1], rect[3])
            rect = QtCore.QRectF(QtCore.QPointF(x1 - 0.2, y1 - 0.2), QtCore.QPointF(x2 + 0.2, y2 + 0.2))
            print rect
            if view.scan:
                view.ScanHandler2(self.lasers[i], rect)
            else:
                view.ScanHandler(self.lasers[i], rect)
                view.rotate(ROTATE[i])
        self.setWindowState(Qt.WindowMaximized)
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    gui = QCheck()
    gui.exec_()
    app.exec_()
