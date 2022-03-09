#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
file: client.py
socket client
"""

import socket
import sys
import cv2

def socket_client():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 6666))
        #connection = s.makefile('wb')
        
    except socket.error as msg:
        print msg
        sys.exit(1)
    print s.recv(1024)
    try:
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90] #设置编码参数
        while ret:
            ret, frame = cap.read()
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
            frame = cv2.resize(frame, (320, 240))
            #转换为jpg格式
            img_str = cv2.imencode('.jpg', frame)[1].tostring()
            # 首先发送图片编码后的长度
            s.send(str(len(img_str)).ljust(16))
            # 然后一个字节一个字节发送编码的内容
            for i in range (0,len(img_str)):
                s.send(img_str[i])
            ret, frame = cap.read()
            if cv2.waitKey(10) == 27:
                break
            # 接收server发送的返回信息
            data_r = s.recv(50)
            print (data_r)
            
    except Exception as e:
        print(e)
    finally:
        s.close()

if __name__ == '__main__':
    socket_client()