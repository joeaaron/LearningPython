#!/usr/bin/env python

 ############################################################
 #  Created on: 2013.04                                     #
 #  Author: LIAO Wenlong                                    #
 #  Email:  Volans.liao@gmail.com                           #
 #  This is part of the Localize and Navigation Toolkit     #
 ############################################################

from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtCore import Qt
import sys, math, copy, threading
from math import sin, cos, atan2


class LaserScan (QtGui.QGraphicsItem):
    Type = QtGui.QGraphicsItem.UserType + 3

    def __init__(self, scan, resolution = 0.1, rect = None):
        super(LaserScan, self).__init__()
        self.setAcceptDrops(False)
        self.scan = scan
        self.resolution = resolution
        self.zone = rect
        self.normalize()

    def normalize(self):
        self.points = QtGui.QPolygonF()
        self.colors = []
        minx, miny, maxx, maxy = 1000, 1000, -1000, -1000

        index = 0
        for p in self.scan:
            index = index + 1
            if abs(p[0]) < 0.01 or abs(p[1]) < 0.01: continue
            if abs(p[0]) > 5 or abs(p[1]) > 5: continue
            lx = p[0]
            ly = p[1]
            lx /= self.resolution
            ly /= self.resolution
            self.points.append( QtCore.QPointF(lx, ly) )
            if index < 640: color = Qt.green
            elif index < 1280: color = Qt.red
            elif index < 1920: color = Qt.blue
            else: color = Qt.green
            self.colors.append(color)
            if self.zone and QtCore.QPointF(lx*self.resolution, ly*self.resolution) not in self.zone: 
                continue
            if (lx > maxx): maxx = lx;
            if (lx < minx): minx = lx;
            if (ly > maxy): maxy = ly;
            if (ly < miny): miny = ly;
        
        self.rect = QtCore.QRectF(minx, miny, maxx - minx, maxy - miny)

    def type(self):
        return LaserScan.Type

    def boundingRect(self):
        return self.rect

    def paint(self, qp, option, widget):
        pen = QtGui.QPen(Qt.lightGray, Qt.DashLine)
        pen.setWidth(1);  
        qp.setPen(pen)
        for j in range(-10, 10):
            i = j * 0.1
            qp.drawLine(QtCore.QPointF(-1, i)/self.resolution, QtCore.QPointF(1, i)/self.resolution);  
        for j in range(-10, 10):
            i = j * 0.1
            qp.drawLine(QtCore.QPointF(i, -1)/self.resolution,QtCore.QPointF(i, 1)/self.resolution);
        
        pen = QtGui.QPen(Qt.red, Qt.DashLine)
        pen.setWidth(1);
        qp.setPen(pen)
        qp.drawLine(QtCore.QPointF(-1, 0)/self.resolution, QtCore.QPointF(1, 0)/self.resolution);  
        qp.drawLine(QtCore.QPointF(0, -1)/self.resolution, QtCore.QPointF(0, 1)/self.resolution); 
        
        for i in range(0, len(self.points)):
            pen = QtGui.QPen(self.colors[i])
            pen.setWidth(3);
            qp.setPen(pen)
            qp.drawPoint(self.points[i])
        

class GraphWidget(QtGui.QGraphicsView):
    resolution = 0.005
    focusOnRobot = False
    showHistoryRobot = True
    historyRobotItemList = []
    
    def __init__(self, parent):
        super(GraphWidget, self).__init__()
        self.scene = QtGui.QGraphicsScene(self)
        self.setScene(self.scene)

        self.scale(1,-1)
        self.setCacheMode(QtGui.QGraphicsView.CacheBackground)
        self.setViewportUpdateMode(QtGui.QGraphicsView.BoundingRectViewportUpdate)
        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)
        self.setDragMode(QtGui.QGraphicsView.ScrollHandDrag);
        self.setBackgroundBrush( QtGui.QBrush(QtGui.QColor(240,  240, 240), Qt.Dense3Pattern)) ;

        self.scan = None
        self.scan2 = None
    def wheelEvent(self, event):
        self.scaleView(math.pow(2.0, event.delta() / 240.0))

    def scaleView(self, scaleFactor):
        factor = self.matrix().scale(scaleFactor, scaleFactor).\
                mapRect(QtCore.QRectF(0, 0, 1, 1)).width()
        if factor < 0.01 or factor > 100:
            return
        self.scale(scaleFactor, scaleFactor)

    def zoom (self, num):
        factor = pow(2.713,num/50.0);
        nowFactor = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1)).width();
        if (factor < 0.07 or factor > 100):
            return;
        self.scale(factor/nowFactor, factor/nowFactor);

    def ScanHandler(self, scan, rect = None):
        if self.scan != None:
            self.scene.removeItem(self.scan)
            self.scan = None

        self.scan = LaserScan(scan, self.resolution, rect )
        self.scene.addItem(self.scan)
    
    def ScanHandler2(self, scan, rect = None):
        if self.scan2 != None:
            self.scene.removeItem(self.scan2)
            self.scan2 = None

        self.scan2 = LaserScan(scan, self.resolution, rect )
        self.scene.addItem(self.scan2)    

