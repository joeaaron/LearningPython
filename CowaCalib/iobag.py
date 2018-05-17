#!/usr/bin/env python
# -*- coding: UTF-8 -*-
 ############################################################
 #  Created on: 2018.04                                     #
 #  Author: cowa                                            #
 #  Email:  aaron.pan@cowarobot.com                         #
 ############################################################
import socket, struct , time
class IO:
    bits = 0x00
    def __init__(self):
        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.s.connect(('192.168.1.75', 502))
    def DO(self, bit, _do): 
        if bit <= 8:
            data = struct.pack('B', _do)
        elif bit <= 16:
            data = struct.pack('H', _do)
        return '\x00\x00\x00\x00\x00' + chr(len(data) + 7) + '\x01\x0F\x00\x00\x00' + chr(bit) + '\x01' + data
    
    #start
    def set(self, bit, flag):
        if flag:
            self.bits = self.bits | (1<<bit)
        else:
            self.bits = self.bits & ~(1<<bit) 
        
    #上下有三个液压开关控制5
    def work_ud(self, pos):
        center = 1
        up = 5
        down = 4
        #下
        if pos == 0:
            self.set(down, 0)
            self.set(up, 1)
            self.set(center, 1)
        elif pos == 1:
            self.set(down, 0)
            self.set(up, 0)
            self.set(center, 0)     
        #上
        elif pos == 2:
            self.set(up, 0)
            self.set(center, 1)
            self.set(down, 1)
        elif pos == 3:
            self.set(up, 0)
            self.set(down, 0)
            self.set(center, 0)
        self.s.send(self.DO(8, self.bits)) 
        time.sleep(3)
        
    #左右只有两个液压开关控制
    def work_lr(self,pos):
        left = 6
        right = 7
        #左
        if pos == 0:
            self.set(right, 0)
            self.set(left, 1)
        elif pos == 1:
            self.set(left, 0)
            self.set(right, 0)
        #右
        elif pos == 2:
            self.set(left, 0)
            self.set(right, 1)
        elif pos == 3:
            self.set(left, 0)
            self.set(right, 0)
        self.s.send(self.DO(8, self.bits)) 
        time.sleep(3)
        
          
    #行李箱拉杆左右只有两个液压开关控制
    def suitcase_lr(self,pos):
        left = 0
        right = 2
        #左
        if pos == 0:
            self.set(right, 0)
            self.set(left, 1)
        elif pos == 1:
            self.set(left, 0)
            self.set(right, 0)
        #右
        elif pos == 2:
            self.set(left, 0)
            self.set(right, 1)
        elif pos == 3:
            self.set(left, 0)
            self.set(right, 0)
        self.s.send(self.DO(8, self.bits)) 
        time.sleep(3)
            
#test

'''
io = IO()

#up
io.work_ud(2)
time.sleep(2)  #延时5s

#down
io.work_ud(0)
time.sleep(2)

#middle
io.work_ud(1)
time.sleep(2)

#left
io.work_lr(0)
time.sleep(2)

#right
io.work_lr(2)
time.sleep(2)

#middle
io.work_lr(1)
time.sleep(2)
'''

'''
for i in range(0, 100):
    io.work_lr(i % 4)
    io.work_ud(i % 4)
    time.sleep(1)
'''

   