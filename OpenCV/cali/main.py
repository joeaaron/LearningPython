#!/usr/bin/env python
# -*- coding: UTF-8 -*-
 ############################################################
 #  Created on: 2017.06                                     #
 #  Author: LIAO Wenlong                                    #
 #  Email:  Volans.liao@gmail.com                           #
 ############################################################
import sys, math, copy, threading, struct, socket, ConfigParser, time, os
import pickle
from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtCore import Qt, QByteArray, QString, QEvent, QTime
from PyQt4.QtNetwork import *  
from PyQt4.QtGui import QMessageBox, QInputDialog, QPlainTextEdit, QPalette, QTextCursor, QKeyEvent, QFileDialog
import time, shutil, zipfile
import numpy as np

import R1Debug, R1Shell
import scipy.misc
from motion import *
from check import *
import ip_h3c

def P2P(axis, pos, vel):
    if motion_axis_p2p(axis, pos, vel): return False
    time.sleep(0.5)
    if motion_axis_wait_finished(axis): return False  
    return True

class QMainWindow(QtGui.QMainWindow):
    R1 = None
    tasks = []
    ssh = None
    ledon = False
    image = None
    h3c = ip_h3c.H3CRouter()
    def showIP(self):
        self.ui.ips.clear()
        for i in self.h3c.listHost():
            item = QtGui.QListWidgetItem(i)
            current_time = QTime.currentTime()
            self.ui.ips.addItem(item)
            self.ui.ips.addItem(current_time)
    def __init__(self, *args ):
        super(QMainWindow, self).__init__()   
        self.XAdd = lambda: motion_axis_move(X, int(self.ui.RSpeed.value() * SPD[X]))
        self.XDec = lambda: motion_axis_move(X, -int(self.ui.RSpeed.value() * SPD[X]))
        self.XStop = lambda: motion_axis_move(X, 0)
        self.YAdd = lambda: motion_axis_move(Y, int(self.ui.RSpeed.value() * SPD[Y]))
        self.YDec = lambda: motion_axis_move(Y, -int(self.ui.RSpeed.value() * SPD[Y]))
        self.YStop = lambda: motion_axis_move(Y, 0) 
        self.ZAdd = lambda: motion_axis_move(Z, int(self.ui.RSpeed.value() * SPD[Z]))
        self.ZDec = lambda: motion_axis_move(Z, -int(self.ui.RSpeed.value() * SPD[Z]))
        self.ZStop = lambda: motion_axis_move(Z, 0)    
        self.PitchAdd = lambda: motion_axis_move(4, int(self.ui.RSpeed.value() * SPD[4]))
        self.PitchDec = lambda: motion_axis_move(4, -int(self.ui.RSpeed.value() * SPD[4]))
        self.PitchStop = lambda: motion_axis_move(4, 0)    
        self.RowAdd = lambda: motion_axis_move(5, int(self.ui.RSpeed.value() * SPD[5]))
        self.RowDec = lambda: motion_axis_move(5, -int(self.ui.RSpeed.value() * SPD[5]))
        self.RowStop = lambda: motion_axis_move(5, 0)      
        self.RAdd = lambda: motion_axis_move(R, int(self.ui.RSpeed.value() * SPD[R]))
        self.RDec = lambda: motion_axis_move(R, -int(self.ui.RSpeed.value() * SPD[R]))
        self.RSTop = lambda: motion_axis_move(R, 0)
        self.RAdd15 = lambda: motion_axis_p2p(R, motion_axis_position(R) + DELTAR15, SPD[R])
        self.RDec15 = lambda: motion_axis_p2p(R, motion_axis_position(R) - DELTAR15, SPD[R])
        self.RowAdd15 = lambda: motion_axis_p2p(4, motion_axis_position(4) + DELTARow15, SPD[4])
        self.RowDec15 = lambda: motion_axis_p2p(4, motion_axis_position(4) - DELTARow15, SPD[4])
        self.PAdd15 = lambda: motion_axis_p2p(5, motion_axis_position(5) + DELTAP15, SPD[5])
        self.PDec15 = lambda: motion_axis_p2p(5, motion_axis_position(5) - DELTAP15, SPD[5])
            
        self.ui = uic.loadUi('ui/main.ui', self)
        try:
            controller_connect('127.0.0.1', 9000)
            controller_lock()
            self.LED = lambda flag: set_digital_output([flag, flag, flag]) 
            self.LED(0)
        except:
            QMessageBox.information(self, u"Error", u"运动控制未连接", QMessageBox.Yes)
        for i in range(0, len(camera1)):
            camera1[i][R] += ROffset
            camera2[i][R] += ROffset
            camera4[i][R] += ROffset
            camera1[i][X] += XOffset
            camera2[i][X] += XOffset
            camera4[i][X] += XOffset
            camera1[i][Y] += YOffset
            camera2[i][Y] += YOffset
            camera4[i][Y] += YOffset
        timer = QtCore.QTimer(self);
        timer.timeout.connect(self.showIP);
        timer.start(3000);
        
        timer2 = QtCore.QTimer(self);
        timer2.timeout.connect(self.CheckLog);
        timer2.start(1000); 
        
        self.showIP()
    def Enable(self):
        print 'enable'
        for i in range(0, 6): motion_axis_enable(i)
    def Disable(self):
        print 'disable'
        for i in range(0, 6): motion_axis_disable(i)
    def Home(self):
        self.Enable()
        print 'home', self.ui.HomeX.isChecked(), self.ui.HomeY.isChecked(), self.ui.HomeZ.isChecked()
        
        if self.ui.HomeZ.isChecked():
            self.PanZero()
            print 'PAN finised'
        
        if self.ui.HomeZ.isChecked():
            motion_axis_home(Z)
            time.sleep(0.5)
            motion_axis_wait_finished(Z)
            print 'Z homed'
        
        if self.ui.HomeY.isChecked():
            motion_axis_home(Y)
            time.sleep(0.5)
            motion_axis_wait_finished(Y)
            print 'Y homed'
        
        if self.ui.HomeX.isChecked():
            motion_axis_home(X)
            time.sleep(0.5)
            motion_axis_wait_finished(X)
            print 'X homed'
        
        if motion_axis_position(R)[1] == 0:
            motion_axis_move(R, SPD[R])
            time.sleep(2)
            motion_axis_move(R, 0)
        if self.ui.HomeX.isChecked() and self.ui.HomeY.isChecked() and self.ui.HomeZ.isChecked():
            self.Move2Zero()
        QMessageBox.information(self, u"OK", u"找零点完成", QMessageBox.Yes)
    def Zero(self):
        if self.Move2Zero():
            QMessageBox.information(self, u"OK", u"回零点完成", QMessageBox.Yes)
            return True
        QMessageBox.information(self, u"错误", u"运动控制错误", QMessageBox.Yes)

    def PanZero(self):
        if motion_axis_p2p(4, ZERO[4], SPD[4]): return False
        if motion_axis_p2p(5, ZERO[5], SPD[5]): return False
        if motion_axis_wait_finished(4): return False
        if motion_axis_wait_finished(5): return False
        return True
    def Move2Zero(self):
        self.Enable()
        if not P2P(Z, ZERO[Z], SPD[Z]): return False
        if not P2P(X, ZERO[0], SPD[X]): return False
        if not self.PanZero(): return False
        if not P2P(R, ZERO[R], SPD[R]): return False
        if not P2P(Y, ZERO[Y], SPD[Y]): return False
        print 'Zero done'
        return True
    def RecordPos(self):
        text = ''
        for i in range(0, 6) : text = text + (', %d'%motion_axis_position(i))
        print text
        text = text[2:]
        self.ui.echo.setText(text)
    def GotoPos(self):
        pos = self.ui.echo.text().toAscii().split(',')
        for i in range(0, 6): 
            print pos[i]
            motion_axis_p2p(i, int(pos[i]), SPD[i])
    def SwitchLed(self):
        if self.ledon: 
            self.ledon = False
            self.LED(0)
        else: 
            self.ledon = True
            self.LED(1)
        
    def Target(self, pos):
        for i in [0, 1, 2, 3, 4, 5]:
            if motion_axis_p2p(i, pos[i], SPD[i]): return False
        time.sleep(0.5)
        for i in range(0, 6):
            if motion_axis_wait_finished(i): return False
        
        print pos, 'arrived'
        return True
    def GetImgSaveByIdx(self, id, index):
        dir = 'image/%d'%(id + 1)
        if index < 5:
            self.LED(1); time.sleep(1)
            if not self.GetImage(id + 0, '%s/x%d.bmp'%(dir, index * 2 + 1)):
                return False
            self.LED(0); time.sleep(1)
            if not self.GetImage(id + 8, '%s/x%d.bmp'%(dir, index * 2 + 2)):
                return False
        elif index == 5:
            self.LED(1); time.sleep(1)
            if not self.GetImage(id, '%s/x%d.bmp'%(dir, 11)):
                return False
        elif index == 6:
            self.LED(1); time.sleep(1)
            if not self.GetImage(id, '%s/x%d.bmp'%(dir, 12)):
                return False
        return True
    def Run(self):
        self.ClearDir()
        for index in range(0, 7):
            if not self.Target(camera1[index]):
                QMessageBox.information(self, u"错误", u"运动控制错误", QMessageBox.Yes); 
                return
            if not self.GetImgSaveByIdx(0, index):
                QMessageBox.information(self, u"错误", u"箱子连接错误", QMessageBox.Yes); 
                return
                
        for index in range(0, 7):
            if not self.Target(camera2[index]):
                QMessageBox.information(self, u"错误", u"运动控制错误", QMessageBox.Yes); 
                return
            if not self.GetImgSaveByIdx(1, index):
                QMessageBox.information(self, u"错误", u"箱子连接错误", QMessageBox.Yes); 
                return                                                                                                            

        if not P2P(Z, camera4[0][Z], SPD[Z]):QMessageBox.information(self, u"错误", u"运动控制错误", QMessageBox.Yes); return
        if not P2P(R, camera4[0][R], SPD[R]):QMessageBox.information(self, u"错误", u"运动控制错误", QMessageBox.Yes); return
        for index in range(0, 7):
            if not self.Target(camera4[index]):
                QMessageBox.information(self, u"错误", u"运动控制错误", QMessageBox.Yes); 
                return
            if not self.GetImgSaveByIdx(3, index):
                QMessageBox.information(self, u"错误", u"箱子连接错误", QMessageBox.Yes); 
                return   
        self.LED(0)
        self.StartCalc()

        if not self.Move2Zero():QMessageBox.information(self, u"错误", u"运动控制错误", QMessageBox.Yes) ; return
        
        self.WaitCalc()
        try:
            print 'file 1 transfering'
            self.ssh.firmware_put('image\\transformationTable1.bin', '/data/cowa_cam_config/transformationTable1.bin')
            print 'file 2 transfering'
            self.ssh.firmware_put('image\\transformationTable2.bin', '/data/cowa_cam_config/transformationTable2.bin')
            print 'file 4 transfering'
            self.ssh.firmware_put('image\\transformationTable4.bin', '/data/cowa_cam_config/transformationTable4.bin')
            print 'file all transfered'
            
            self.R1.closeCamera()
            time.sleep(1)
            pid = self.ssh.run('ps | grep cowarobot')
            while '  ' in pid:
                pid = pid.replace('  ', ' ')
            pid = pid.split(' ')[1]
            self.ssh.run('kill -9 %s'%pid)
            print 'cowarobot reboot done'
            
            time.sleep(1)
            ip = str(self.ui.IP.text()).strip()
            self.R1 = R1Debug.R1Debug(ip)
            self.R1.openCamera()
            print 'reconnected'
        except:
            QMessageBox.information(self, u"错误", u"标定过程完成， 文件传输错误", QMessageBox.Yes)
            return
        if self.Check():
            QMessageBox.information(self, u"OK", u"标定完成", QMessageBox.Yes)
        if not self.Move2Zero():QMessageBox.information(self, u"错误", u"运动控制错误", QMessageBox.Yes) ; return
        self.Zip()
        self.LED(1)
    def Check(self):
        lasers = []
        for pos in LaserTestPos:
            if not self.Target(pos):
                QMessageBox.information(self, u"错误", u"运动控制错误", QMessageBox.Yes); 
                return False
            try:
                laser = self.R1.requestLaser()
            except:
                laser = ''
            if not len(laser):
                QMessageBox.information(self, u"错误", u"箱子连接错误", QMessageBox.Yes); 
                return False
            lasers.append(laser)
        pickle.dump(lasers, open("image\\check.dat", "wb"))
        
        print u'开始质检'
        win = QCheck(self, lasers)
        win.exec_()
        return True
        
        Error = lambda(x): QMessageBox.information(self, u"错误", u"标定不成功，请重新标定，如多次不成功请联系研发工程师。", QMessageBox.Yes)
        for idx in range(0, len(lasers)):
            cfg = LaserTestCfg[idx]
            if len(cfg) < 4:
                if cfg == (1,4):
                    first = lasers[idx][640-80:640]
                    second = lasers[idx][640:640+80]
                if cfg == (1,2):
                    first = lasers[idx][1280-80:1280]
                    second = lasers[idx][1280:1280+80]
                x = 0; y = 0; size = 0
                for i in first:
                    if abs(i[0]) < 0.01 or abs(i[1]) < 0.01: continue
                    if abs(i[0]) > 2.50 or abs(i[1]) > 2.50: continue
                    x = x + i[0]
                    y = y + i[1]
                    size = size+1
                if size < 4: Error(0); return False
                
                def dist(x, y): return np.sqrt(x*x+y*y)
                r1 = dist(x/size, y/size)
                
                #print second
                x = 0; y = 0; size = 0
                for i in second:
                    if abs(i[0]) < 0.01 or abs(i[1]) < 0.01: continue
                    if abs(i[0]) > 2.50 or abs(i[1]) > 2.50: continue
                    x = x + i[0]
                    y = y + i[1]
                    size = size+1
                if size < 4: Error(0); return False
                r2 = dist(x/size, y/size) 
                print 'laser: ', r1 - r2
                if abs(r1 - r2) > 0.1:Error(1); return
                continue
            camera, A, B, revert = cfg
            if camera == 1: laser = lasers[idx][640:1280]
            elif camera == 2: laser = lasers[idx][1280:1920]
            elif camera == 3: laser = lasers[idx][1920:]
            elif camera == 4: laser = lasers[idx][0:640]
            X = [] 
            Y = []
            for i in laser:
                if abs(i[0]) < 0.01 or abs(i[1]) < 0.01: continue
                if abs(i[0]) > 2.50 or abs(i[1]) > 2.50: continue
                if not revert:
                    x = i[0]
                    y = i[1]
                else:
                    x = i[1]
                    y = i[0]
                if abs(A * x + B - y) > 0.5: continue
                X.append(x)
                Y.append(y)
                #print x, y
            P, V = np.polyfit(X, Y, 1, cov = True) 
            err = abs(A - P[0]) + abs(B - P[1])
            conv = V[0][0]*V[0][0] + V[1][1]*V[1][1] - 2*V[1][1]*V[0][0]
            if len(X) < 80: Error(1); return
            print 'laser: ', err, conv
            if err > 0.2 or conv > 1e-8: Error(1); return

        return True
    def Connect(self):
        ip = str(self.ui.IP.text()).strip()
        try:
            self.R1 = R1Debug.R1Debug(ip)
            self.R1.openCamera()
            print 'camera opened'
            
            self.ssh = R1Shell.Shell()
            self.ssh.login(ip)
        except:
            QMessageBox.information(self, u"OK", u"连接失败", QMessageBox.Yes)
            return
        
        file = self.ssh.run('cat /data/config.ini')
        if '"camera_test_count":\t1' not in file:
            QMessageBox.information(self, u"OK", u"摄像头未匹配", QMessageBox.Yes)
            return
        QMessageBox.information(self, u"OK", u"%s连接成功"%self.R1.getID(), QMessageBox.Yes)
    def CheckLog(self):
        if not self.R1:
            return
        try:
            out = self.ssh.run('dmesg | grep "WQ ERROR"')
        except:
            self.R1 = None
            return
        if len(out) > 3:
            open('backup\\%s_cam.log'%self.R1.getID(), 'wb').write(out)
            for i in range(0, 6):
                motion_axis_move(i, 0)
            QMessageBox.information(self, u"OK", u"摄像头丢帧", QMessageBox.Yes)
    def GetImage(self, cam, file):
        if self.R1 == None:
            return False
        try:
            image = self.R1.requestImage(cam)
        except:
            return False
        if len(file):
            scipy.misc.imsave(file, image) 
        else:
            return image
        return True
    def GetLaser(self):
        laser = self.R1.requestLaser()
        self.ui.plot.ScanHandler(laser)
    def ShowImage(self):
        idx = int(self.ui.camIndex.currentText()) - 1
        print idx
        image = self.R1.requestImage(idx)
        print len(image)
        image = QtGui.QImage(image, image.shape[1], image.shape[0], image.shape[1],QtGui.QImage.Format_Indexed8 )
        pix = QtGui.QPixmap(image)
        if self.image:
            self.ui.plot.scene.removeItem(self.image)
        self.image = self.ui.plot.scene.addPixmap(pix)
        
    def StartCalc(self):
        self.tasks = []
        for i in [1, 2, 4]:
            #delOut('image/%d'%i)  
            calibrate = lambda cam: os.system('bin\\calibrate.exe image %d'%cam)
            task = threading.Thread(target=calibrate, args=(i,))
            task.start()
            self.tasks.append(task)
    def WaitCalc(self):
        for task in self.tasks:
            task.join()
        shutil.copy('image\\1\\transformationTable.bin', 'image\\transformationTable1.bin')
        shutil.copy('image\\2\\transformationTable.bin', 'image\\transformationTable2.bin')
        shutil.copy('image\\4\\transformationTable.bin', 'image\\transformationTable4.bin')

    def CalibrateCalc(self):
        self.StartCalc()
        self.WaitCalc() 
        
    def ClearDir(self):
        try:shutil.rmtree('image')
        except: pass
        try: os.makedirs('image')
        except: pass
        os.makedirs('image\\1')
        os.makedirs('image\\2')
        os.makedirs('image\\4')
    def Zip(self):
        for i in [1, 2, 4]:
            path = 'image/%d'%i
            for file in os.listdir( path ) :  
                f = os.path.join( path, file )  
                if True in map( file.endswith, ('.xml', '.bin', '.txt') ): os.remove( f )
        id = self.R1.getID()
        #backup = time.strftime("backup\\%y.%m.%d %H.%M.zip", time.localtime()) 
        backup = "backup\\%s.zip"%id
        f = zipfile.ZipFile(backup,'w', zipfile.ZIP_DEFLATED)
        for dirpath, dirnames, filenames in os.walk('image'):
            for filename in filenames:
                f.write(os.path.join(dirpath,filename))
        f.close()
if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    gui = QMainWindow()#Widget()
    
    gui.show()
    app.exec_()
