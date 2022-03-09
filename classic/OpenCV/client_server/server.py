#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import threading
import time
import sys
import numpy
import cv2

# 接受图片大小的信息
def recv_size(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

# 接收图片
def recv_all(sock, count):
    buf = ''
    while count:
        # 这里每次只接收一个字节的原因是增强python与C++的兼容性
        # python可以发送任意的字符串，包括乱码，但C++发送的字符中不能包含'\0'，也就是字符串结束标志位
        newbuf = sock.recv(1)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf
    
def socket_service():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 防止socket server重启后端口被占用（socket.error: [Errno 98] Address already in use）
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('127.0.0.1', 6666))
        s.listen(10)
        
        #connection = s.accept()[0].makefile('rb')
        
    except socket.error as msg:
        print msg
        sys.exit(1)
    print 'Waiting connection...'

    while 1:
        conn, addr = s.accept()
        t = threading.Thread(target=deal_data, args=(conn, addr))
        t.start()

def deal_data(conn, addr):
    print 'Accept new connection from {0}'.format(addr)
    conn.send('Hi, Welcome to the server!')
    while 1:
        length = recv_size(conn,16)
        if isinstance(length,str):
            stringData = recv_all(conn,int(length))
            data = numpy.fromstring(stringData, dtype='uint8')
            decimg=cv2.imdecode(data,1)
            cv2.imshow('SERVER',decimg)
            if cv2.waitKey(10) == 27:
                break
            print('Image recieved successfully!')
            conn.send("Server has recieved messages!")
        if cv2.waitKey(10) == 27:
            break 
    conn.close()
    cv2.destroyAllWindows();

if __name__ == '__main__':
    socket_service() 