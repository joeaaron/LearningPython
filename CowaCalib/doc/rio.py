import socket, struct , time
class AIO:
    bits = 0x00
    def __init__(self, addr = '192.168.1.75'):      
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.s.connect((addr, 502) )
    def AO(self, ch, v): 
        d = '\x00\x00\x00\x00\x00' + '\x06' + '\x01\x06' + struct.pack('>HH', ch, v)
        self.s.send(d)

    def DO(self, bit, _do): 
        if bit <= 8:
            data = struct.pack('B', _do)
        elif bit <= 16:
            data = struct.pack('<H', _do)
        return '\x00\x00\x00\x00\x00' + chr(len(data) + 7) + '\x01\x0F\x00\x00\x00' + chr(bit) + '\x01' + data
    def setDO(self, bit, flag):
        if not flag: self.bits = self.bits & ~(1<<bit) 
        else: self.bits = self.bits | (1<<bit)
        self.s.send(self.DO(16, self.bits))
    def workon(self):
        self.bits = (self.bits | 0x01 | 0x04) & ~0x02# work on
        self.s.send(self.DO(16, self.bits))
    def workoff(self):
        self.bits = (self.bits & ~(0x01 | 0x04)) | 0x02 #workoff
        self.s.send(self.DO(16, self.bits))
    def backward(self):
        self.bits = self.bits | (1<<3) #backward
        self.s.send(self.DO(16, self.bits))
    def forward(self):
        self.bits = self.bits & ~(1<<3) #forward
        self.s.send(self.DO(16, self.bits))
    def power(self, flag = 1):
        if flag:
            self.bits = self.bits | (1<<4)
        else:
            self.bits = self.bits & ~(1<<4)
        self.s.send(self.DO(16, self.bits))

if __name__=="__main__":
    
    aio = AIO()
    dio = aio
    aio.AO(0, 0)
    dio.power(0)
    time.sleep(1)
    dio.forward()
    dio.power(1)
    time.sleep(1)
    
    while 1:
        a = raw_input()
        if 'v' in a:
            aio.AO(0, int(a[1:]) * 5000)
        elif 'off' in a:
            dio.power(0)
        elif 'on' in a:
            dio.power(1)
        elif 'back' in a:
            dio.backward()
        elif 'for' in a:
            dio.forward() 
        elif 'work' in a:
            dio.workon()
        elif 'un' in a:
            dio.workoff()
            print '--------'
