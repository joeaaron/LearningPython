import socket, struct, threading, time, Queue, traceback
from PIL import Image
import numpy as np
import scipy.misc

CMD_HEARTBEAT = 0	#"hello world" test cmd to check communication
CMD_ACCMD = 1		#check if cmd is supported 
CMD_CAMERA = 2		#cmd about camera
CMD_LOG = 3		#cmd print log info
CMD_REGISTER = 4	#cmd register camera
CMD_MODBUS = 5		#cmd about modbus
CMD_SHELL = 6		#cmd shell command
CMD_TOP_LASER = 7		#cmd about top laser data
CMD_BOTTOM_LASER = 8   #cmd about bottm laser data
CMD_ALL_LASER = 9      #cmd about all laser
CMD_LASERPRO = 14
CMD_SUITECASE = 15

CMD_PARAMETER_NULL = 0,			#no parameter
CMD_CAMERA_OPEN=1,				#parameter open camera
CMD_CAMERA_CLOSE=2,				#parameter close camera
CMD_CAMERA_BLACK=3,				#parameter get a totally black image
CMD_CAMERA_WHITE=4,				#parameter get a totally white image
CMD_CAMERA_TEST=5,				#parameter get a prescribed image
CMD_CAMERA_DATA=6,				#parameter get image data
CMD_LASER_ON=7,                   #open all the lasers
CMD_LASER_OFF=8,                  #close all the lasers
CMD_TOP_LASER_ON=9,
CMD_BOTTOM_LASER_ON=10,
CMD_TOP_FALL_LASER_ON=11,
CMD_BOTTOM_FALL_LASER_ON=12,
CMD_LASER_DATA=13,
CMD_LASER_TEST=14,
CMD_LASER_CLEAR=15,
CMD_SUITECASE_NUM = 16
CMD_REGISTER_LASER = 0x3005 	#register addr of laser:set 8,laser on,set 0,laser off
CMD_REGISTER_EXPOSURE = 0x3501	#register addr of exposure value, range:0 ~ 255
CMD_REGISTER_GAIN = 0x350b		#register addr of gain value, range:0 ~ 255

pack = lambda id, str: struct.pack('>hi', id, len(str)) + str
class R1Debug:
    isRunning = True
    def __init__(self, ip, port = 6000):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, port))
        
        print 'connected'
        
        self.queue = Queue.Queue()
        #self.lock = threading.Condition()
        self.task = threading.Thread(target = self.update)
        self.task.start()
    def openCamera(self):
        cmd = pack(CMD_CAMERA, 'AC+OPEN')
        self.sock.sendall(cmd)
        self.wait(CMD_CAMERA)
        
        cmd = pack(CMD_REGISTER, struct.pack('>ii', CMD_REGISTER_GAIN, 5))
        self.sock.sendall(cmd)
        self.wait(CMD_REGISTER)
        
        cmd = pack(CMD_REGISTER, struct.pack('>ii', CMD_REGISTER_EXPOSURE, 10))
        self.sock.sendall(cmd)
        self.wait(CMD_REGISTER)
    def closeCamera(self):
        cmd = pack(CMD_CAMERA,'AC+CLOSE')
        self.sock.sendall(cmd)
    def requestImage(self, index):
        self.clear()
        cmd = pack(CMD_CAMERA,'AC+DATA %d'%index)
        self.sock.sendall(cmd)
        data = self.wait(CMD_CAMERA)
        if len(data) == 0: return None
        id, w, h = struct.unpack('>hhh', data[0:6])
        print id, w, h
        data = np.fromstring(data[6:], dtype=np.uint8)
        return data.reshape(h, w)
    def requestLaser(self):
        self.clear()
        cmd = pack(CMD_LASERPRO, 'AC+DEBUG_MODE_ON2')
        
        self.clear()
        cmd = pack(CMD_TOP_LASER, 'AC+LASER_DATA')
        self.sock.sendall(cmd)
        data = self.wait(CMD_TOP_LASER)
        if len(data) == 0: return None
        data = struct.unpack('<%dh'%(len(data)/2), data)
        if len(data) % 2 == 1: return None
        laser = [(data[2*i] / 1000.0, data[2*i + 1] / 1000.0) for i in range(0, len(data) / 2)]
        
        self.clear()
        cmd = pack(CMD_LASERPRO, 'AC+DEBUG_MODE_ON1')
        return laser
    def verbose(self):
        cmd = pack(CMD_HEARTBEAT,'fuck u')
        self.sock.sendall(cmd)
        print self.wait(CMD_HEARTBEAT)
    def clear(self):
        while not self.queue.empty():
            self.queue.get_nowait()
    def wait(self, cmd, timeout = None):
        t = time.time()
        while not self.queue.empty():
            data = self.queue.get_nowait()
            if data[0] == cmd:
                return data[1]
            elif not self.isRunning:
                raise Exception('Socket Error')
        data = self.queue.get(timeout=timeout)
        if data[0] == cmd:
            return data[1]
        elif not self.isRunning:
            raise Exception('Socket Error')
    def parse(self, cmd, data):
        self.queue.put((cmd, data))
    def update(self):
        buffer = ''
        while self.isRunning:
            try:
                buffer += self.sock.recv(1024)
            except:
                self.isRunning = False
                self.queue.put((None, None))
                self.queue.put((None, None))
                self.queue.put((None, None))
                break
            while True:
                if len(buffer) < 6: break
                cmd, length = struct.unpack('>hi', buffer[0:6])
                if len(buffer) < 6 + length: break
                
                if length > 0: data = buffer[6: 6 + length]
                else: data = None
                buffer = buffer[6 + length:]
                
                if data == 'HELLOWORLD': continue
                self.parse(cmd, data)
    def getID(self):
        cmd = pack(CMD_SUITECASE,'AC+GET_ID')
        self.sock.sendall(cmd)
        data = self.wait(CMD_SUITECASE)
        return data
#d = R1Debug('192.168.1.103')
#d.openCamera()
#d.openCamera()
#print 'verbosed'

#scipy.misc.imsave('image/%d.bmp'%1, d.requestImage(9)) 

#while 1:
#    time.sleep(1)
#d.update()

#print `chr(10)`