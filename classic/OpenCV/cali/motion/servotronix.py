import serial, time, socket
drivelogfile = open('drive.log', 'w')
drivelog = lambda s: drivelogfile.write(s + '\n')
class Servotronix(object):
    addr = 0
    net = False
    def __init__(self, port):
        self.ip = port
        if 'COM' in port:
            self.port = serial.Serial(port=port, baudrate=115200, timeout = 0.01)
        else:
            self.port = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.port.settimeout(0.01)
            self.port.connect(port)
            self.net = 1
    def send(self, cmd):
        if self.net: 
            #self.port.recv(1024)
            self.port.sendall(cmd + '\r')
            drivelog( cmd )
        else: 
            self.port.flushInput()
            self.port.write(cmd)
            time.sleep(0.01)
            self.port.write('\r')
    def recv(self, n):
        try: 
            return self.port.recv(1024)
        except:
            return ''
    def select(self, addr):
        if self.addr == addr:
            return True
        for i in range(0, 3):
            self.send('\\%d'%addr)
            buff = ''
            for i in range(0, 15):
                if self.net: buff += self.recv(1024)
                else: buff += self.port.read(1)
                if '\r' in buff: buff = buff.split('\r')[-1]
                try: num = int(buff[:-2])
                except: num = 0
                if '%d->'%(addr) in buff:
                    self.addr = addr
                    return True
                elif buff[-2:]=='->' and num == addr:
                    self.addr = addr
                    return True

        print 'Select ERR2:', buff
        return False
        
    def cmd_return(self, cmd, ret = 0):
        self.send(cmd)
        buff = ''
        for i in range(0, 500):
            if self.net: buff += self.recv(1024)
            else: buff += self.port.read(1)
            if cmd in buff and buff[-2:]=='->':
                drivelog( '%s %d success: %s'%(cmd, self.addr, buff.replace('\r\n', '#')) )
                return buff.split('\r')[1].strip()
        return ''
    def enable(self):
        if len(self.cmd_return('en')):return True
        else: return False
    def disable(self):
        if len(self.cmd_return('k')):return True
        else : return False
    def stop(self):
        if len(self.cmd_return('stop')):return True
        else : return False
    def p2p(self, p, v):
        if v < 0: v = -v
        cmd = "moveabs %d %.2f"%(p, v * 1.0 / 131072 * 60)
        if len(self.cmd_return(cmd, 1)): return True
        else: return False
    def status(self):
        enabled_buff = self.cmd_return('active', 1)[:2]
        if enabled_buff[:2] == '0<': enabled = False
        elif enabled_buff[:2] == '1<': enabled = True
        else: return None
            
        pos_buff = self.cmd_return('pfb', 1).split(' [counts]')
        if len(pos_buff) == 2: pos = float(pos_buff[0])
        else: return None

        finished_buff = self.cmd_return('stopped', 1)
        if '-1<' in finished_buff: finished = False
        elif '0<' in finished_buff: finished = False
        elif '1<' in finished_buff: finished = False
        elif '2<' in finished_buff: finished = True
        return (enabled, finished, int(pos))
    def output(self, flag):
        if flag:
            self.cmd_return('out 8 1')
            self.cmd_return('out 10 1')
        else:
            self.cmd_return('out 8 0')
            self.cmd_return('out 10 0')

DRIVE = [None]*11
AXISDICT = [3, 4, 5, 6, 9, 10]
def controller_connect(addr, port):
    #COM = {'COM7': [3, 4],
    #       'COM5': [5, 6],
    #       'COM9': [9, 10]}
    COM = {('192.168.2.5', 5000): [3, 4],
           ('192.168.2.5', 5100): [5, 6],
           ('192.168.2.5', 5200): [9, 10]}
    for com in COM:
        s = Servotronix(com)
        for axis in COM[com]:
            DRIVE[axis] = s
def controller_lock(): return True
def controller_unlock(): return True
def motion_axis_enable(axis): 
    DRIVE[AXISDICT[axis]].select(AXISDICT[axis])
    return DRIVE[AXISDICT[axis]].enable()
def motion_axis_disable(axis): 
    DRIVE[AXISDICT[axis]].select(AXISDICT[axis])
    return DRIVE[AXISDICT[axis]].disable()
def motion_axis_home(axis): return True
def motion_axis_p2p(axis, p, v):
    DRIVE[AXISDICT[axis]].select(AXISDICT[axis])
    if DRIVE[AXISDICT[axis]].p2p(p, v): return 0
    else: return -1

def motion_axis_wait_finished(axis):
    DRIVE[AXISDICT[axis]].select(AXISDICT[axis])
    while 1:
        status = DRIVE[AXISDICT[axis]].status()
        if status and len(status) == 3:
            if status[1]: return 0
            if not status[0]: return -1
def motion_axis_position(axis):
    DRIVE[AXISDICT[axis]].select(AXISDICT[axis])
    while 1:
        status = DRIVE[AXISDICT[axis]].status()
        if len(status) == 3:
            return status[2]
def motion_axis_move(axis, v):
    DRIVE[AXISDICT[axis]].select(AXISDICT[axis])
    if v == 0: return DRIVE[AXISDICT[axis]].stop()
    elif v > 0: return DRIVE[AXISDICT[axis]].p2p(2147483640, v) 
    elif v < 0: return DRIVE[AXISDICT[axis]].p2p(-2147483640, v) 
def set_digital_output(flag):
    axis = 3
    DRIVE[AXISDICT[axis]].select(AXISDICT[axis])
    DRIVE[AXISDICT[axis]].output(flag[0])
        
if __name__ == '__main__':
    controller_connect('1', 2)
    #print DRIVE
    for i in range(2, 6): motion_axis_enable(i)
    #print DRIVE[2].status()
    for i in range(2, 6): motion_axis_disable(i)