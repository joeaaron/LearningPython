#!/usr/bin/env python
# -*- coding: UTF-8 -*-
 ############################################################
 #  Created on: 2018.04                                     #
 #  Author: cowa                                            #
 #  Update: 2018.05.30
 #  Email:  aaron.pan@cowarobot.com                         #
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
import IOBag
from motion import *
from check import *
import ip_h3c

ALLIP = os.listdir('.\\backup')
ALLIP = [i.replace('.zip', '') for i in ALLIP]

class QMainWindow(QtGui.QMainWindow):
    R1 = None
    tasks = []
    ssh = None
    ledon = False
    image = None
    cameraLog = ''
    io = IOBag.IO()  #气缸控制
    h3c = ip_h3c.H3CRouter()
    def showIP(self):
        self.ui.ips.clear()
        for i in self.h3c.listHost():
            current_time = QTime.currentTime()
            strTime = current_time.toString("h:m:s ap")
            qtime = unicode(strTime)  #curerntTime
            #print strTime
            if not '310' in i: continue
            i = i.split(';')[1:]
            if i[1] in ALLIP: i.append(u'已标定过')
            else: i.append(u'即将标定')
        
            i = '\t'.join(i)
            item = QtGui.QListWidgetItem(i);
            self.ui.ips.addItem(item)
          
    def SetIP(self):
        ip = self.ui.ips.currentItem().text()
        self.ui.IP.setText(ip.split('\t')[0])
        
    def __init__(self, *args ):
        super(QMainWindow, self).__init__()   
        self.ui = uic.loadUi('ui/main.ui', self)
        #装载样示表
        qss_file = open('ui/qdarkstyle/style.qss').read()
        self.setStyleSheet(qss_file)
        try:
            self.LED = lambda flag: self.io.digital_output(flag) 
            self.LED(0)
        except:
            QMessageBox.information(self, u"Error", u"LED打开失败", QMessageBox.Yes)
            
        try:
            self.ROT = lambda sig: self.io.suitcase_90(sig) 
            self.ROT(0)
        except:
            QMessageBox.information(self, u"Error", u"旋转90°失败", QMessageBox.Yes)
        
        
        timer = QtCore.QTimer(self);
        timer.timeout.connect(self.showIP);
        timer.start(3000);
        
        timer2 = QtCore.QTimer(self);
        timer2.timeout.connect(self.CheckLog);
        timer2.start(1000); 
        
        self.showIP()
        
    def SwitchLed(self):
        if self.ledon: 
            self.ledon = False
            self.LED(0)
        else: 
            self.ledon = True
            self.LED(1)
            
    def ChessbMid(self):
        self.Target(1)
        
    def ChessbMid2(self):
        self.io.work_lr(1)
        
    def ChessbUP(self):
        self.Target(0)
    
    def ChessbDOWN(self):
        self.Target(2)
        
    def ChessbLEFT(self):
        self.Target(3)
        
    def ChessbRIGHT(self):
        self.Target(4)  
        
    def SuitMid(self):
        self.io.suitcase_lr(1) 
        
    def RAdd(self):
        self.Target(5)
        
    def RDec(self):
        self.Target(6)
        
    def RAdd90(self):
        if self.rot: 
            self.rot = False
            self.ROT(0)
        else: 
            self.rot = True
            self.ROT(1)
        
    def Zero(self):
        if self.Move2Zero():
            QMessageBox.information(self, u"OK", u"回零点完成", QMessageBox.Yes)
            return True
        QMessageBox.information(self, u"错误", u"运动控制错误", QMessageBox.Yes)

    def Move2Zero(self):
        self.io.work_ud(1)
        self.io.work_lr(1)
        self.io.suitcase_lr(1)
        self.io.suitcase_90(0)
        print 'Zero done'
        return True   
        
    def Target(self, pos):
        
        if pos == 0:
            self.io.work_ud(0)
        elif pos == 1:
            self.io.work_ud(1)           
        elif pos == 2:
            self.io.work_ud(2)
        elif pos == 3:
            self.io.work_lr(0) 
        elif pos == 4:
            self.io.work_lr(2)
        elif pos == 5:
            self.io.suitcase_lr(0)
        elif pos == 6:
            self.io.suitcase_lr(2)
            
        #time.sleep(2)
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
        
    def GetImgSaveByIdxPro(self, id, index):    
        if index < 5:
            self.LED(1); time.sleep(1)
            for i in range(0, len(id)):
                dir = 'image/%d'%(id[i] + 1)
                if not self.GetImage(id[i] + 0, '%s/x%d.bmp'%(dir, index * 2 + 1)):
                    return False
                   
            self.LED(0); time.sleep(1)
            for i in range(0, len(id)):
                dir = 'image/%d'%(id[i] + 1)
                if not self.GetImage(id[i] + 8, '%s/x%d.bmp'%(dir, index * 2 + 2)):
                    return False
                
        elif index == 5:
            self.LED(1); time.sleep(1)
             
            for i in range(0, len(id)):
                dir = 'image/%d'%(id[i] + 1)
                if not self.GetImage(id[i] + 0, '%s/x%d.bmp'%(dir, 11)):
                    return False
                
        elif index == 6:
            self.LED(1); time.sleep(1)
            for i in range(0, len(id)):
                dir = 'image/%d'%(id[i] + 1)
                if not self.GetImage(id[i] + 0, '%s/x%d.bmp'%(dir, 12)):
                    return False
        return True
        
    def PushFiles(self):
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
            self.ssh.run('kill -9 %s' % pid)
            print 'cowarobot reboot done'

            time.sleep(1)
            ip = str(self.ui.IP.text()).strip()
            self.R1 = R1Debug.R1Debug(ip)
            self.R1.openCamera()
            print 'reconnected'
        except:
            QMessageBox.information(self, u"错误", u"标定过程完成， 文件传输错误", QMessageBox.Yes)
            return
            
    def GetBackToNormal(self, index):
        # 棋盘格左右转时，保证棋盘格在中间
        if 2 == index:
            self.io.work_ud(1)
            
        elif 3 == index:
            self.io.work_lr(1) 
            
        # 拉杆左右转时，保证棋盘格在中间
        elif 4 == index:
            self.io.work_lr(1)
        
        elif 5 == index:
            self.io.suitcase_lr(1)
            
        elif 6 == index:
            self.io.suitcase_lr(1)
            
        print 'normal pos arrived'
        return True   
        
    def Run(self):
        '''
        if not self.Target(0):
            QMessageBox.information(self, u"错误", u"运动控制错误", QMessageBox.Yes); 
            return
        if not self.Target(2):
            QMessageBox.information(self, u"错误", u"运动控制错误", QMessageBox.Yes); 
            return
        '''
        #清空文件夹
        self.ClearDir()
        #1，2, 4 号激光摄像头到指定位置拍摄
        for index in range(0, 7):
            #三个轴同时运动
            if not self.Target(index):
                QMessageBox.information(self, u"错误", u"运动控制错误", QMessageBox.Yes); 
                return
            
            if not self.GetImgSaveByIdxPro([0], index):
                QMessageBox.information(self, u"错误", u"箱子连接错误", QMessageBox.Yes); 
                return
                
            if not self.GetBackToNormal(index):
                QMessageBox.information(self, u"错误", u"运动控制错误", QMessageBox.Yes); 
                return
                
     
        # self.io.suitcase_90(1)        #旋转90°
        
        time.sleep(10)
        
        for index in range(0, 7):
            #三个轴同时运动
            if not self.Target(index):
                QMessageBox.information(self, u"错误", u"运动控制错误", QMessageBox.Yes); 
                return
            
            if not self.GetImgSaveByIdxPro([1, 3], index):
                QMessageBox.information(self, u"错误", u"箱子连接错误", QMessageBox.Yes); 
                return
                
            if not self.GetBackToNormal(index):
                QMessageBox.information(self, u"错误", u"运动控制错误", QMessageBox.Yes); 
                return
                
        #关闭光源
        self.LED(0)
        #运行标定程序
        self.StartCalc()
        
        #回零
        if not self.Move2Zero():QMessageBox.information(self, u"错误", u"运动控制错误", QMessageBox.Yes) ; return
        #bin文件拷贝到文件夹外层
        self.WaitCalc()
       
        
        '''
        #标定结果质检
        if self.Check():
            QMessageBox.information(self, u"OK", u"标定完成", QMessageBox.Yes)
        #再次检查回零是否成功
        if not self.Move2Zero():QMessageBox.information(self, u"错误", u"运动控制错误", QMessageBox.Yes) ; return
        #打包
        self.Zip()
        #开灯
        self.LED(1)
        '''
    def Check(self):
        self.PushFiles()
        
        try:
            lasers = self.R1.requestLaser()
        except:
            lasers = ''
        if not len(lasers):
            QMessageBox.information(self, u"错误", u"箱子连接错误", QMessageBox.Yes); 
            return False
        # 将采集到的激光写入文件  
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
        #backup = time.strftime("backup \\%y.%m.%d %H.%M.zip", time.localtime()) 
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
