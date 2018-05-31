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
    
    '''
    #上下有三个液压开关控制
    def work_ud(self, pos):
        center = 1
        up = 5
        down = 4
        #上
        if pos == 0:
            
            self.set(up, 1)
            self.set(down, 0)    
           # time.sleep(5)
           
            self.set(center, 1)
           
        elif pos == 1:
            self.set(center, 0) 
            self.set(down, 0)
            self.set(up, 0)            
        #下
        elif pos == 2:
            self.set(up, 0)
            self.set(down, 1)
            time.sleep(5)
            self.set(center, 1)
            
        elif pos == 3:
            self.set(center, 0)
            self.set(up, 0)
            self.set(down, 0)
           
        self.s.send(self.DO(8, self.bits)) 
        time.sleep(3)
    '''
    #上下液压开关控制
    def ud(self, pos):
        up = 5
        down = 4
        #上
        if pos == 0:
            
            self.set(up, 1)
            self.set(down, 0)    
           
        elif pos == 1:
 
            self.set(down, 0)
            self.set(up, 0)            
        #下
        elif pos == 2:
            self.set(up, 0)
            self.set(down, 1)
                   
        elif pos == 3:   
            self.set(up, 0)
            self.set(down, 0)
           
        self.s.send(self.DO(8, self.bits)) 
        time.sleep(3)
        
    #中间液压开关控制
    def mid(self,pos):
        center = 1
        if pos == 1:
            self.set(center, 1)
       
        elif pos == 0:
            self.set(center, 0)
     
        self.s.send(self.DO(8, self.bits)) 
        time.sleep(1)
    
    def work_ud(self,pos):
        #上
        if pos == 0: 
            self.ud(0)
            self.mid(1)    
           
        elif pos == 1:
            self.ud(1)
            self.mid(0)              
        #下
        elif pos == 2:
            self.ud(2)
            self.mid(1)
                   
        elif pos == 3:   
            self.ud(3)
            self.mid(0) 
            
    #左右只有两个液压开关控制
    def work_lr(self,pos):
        left = 3
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
    
    #行李箱拉杆旋转90°
    def suitcase_90(self,pos):
        rotate = 3
        # 旋转
        if pos == 1:
            self.set(rotate, 1)
        # 不旋转
        elif pos == 0:
            self.set(rotate, 0)
     
        self.s.send(self.DO(8, self.bits)) 
        time.sleep(3)
        
    #红外补光灯的亮灭
    def digital_output(self,signal):
        led = 6
        # 亮
        if signal == 1:
            self.set(led, 1)
        # 灭
        elif signal == 0:
            self.set(led, 0)
     
        self.s.send(self.DO(8, self.bits)) 
        time.sleep(1)
           
#test
'''
io = IO()

#up
io.work_ud(0)
time.sleep(2)

#middle
io.work_ud(1)
time.sleep(2)

#down
io.work_ud(2)
time.sleep(2)  #延时5s

#middle
io.work_ud(1)
time.sleep(2)


io.digital_output(1)
io.digital_output(0)

#left
io.suitcase_lr(0)
time.sleep(2)

#right
io.suitcase_lr(2)
time.sleep(2)

#middle 
io.suitcase_lr(1)
time.sleep(2)

io.suitcase_90(1)
io.suitcase_90(0)
 


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

   