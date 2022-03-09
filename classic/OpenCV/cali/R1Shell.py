import os, re, subprocess, time
import paramiko


class Shell:
    lastHost = []
    ssh = None
    sftp =None
    channel = None
    def login(self, ip):
        self.channel = None
        self.sftp = None
        self.ssh = None
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(ip, port=2223, username = 'root', password = '123456', timeout = 100)
        except:
            return
        self.ssh = ssh
        self.sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
    def run(self, cmd):
        if self.ssh == None:
            return None
        stdin, stdout, stderr = self.ssh.exec_command(cmd); 
        return stdout.read()
    def startIO(self, cmd):
        if self.ssh == None:
            return None
        self.channel = self.ssh.invoke_shell()
    def write(self, cmd):
        if self.ssh == None or self.channel == None:
            return None
        self.channel.send(cmd)
    def wait(self, line, timeout):
        start = time.time()
        buffer = ''
        while line not in buffer:
            str = chan.recv(65535)
            buffer += str
            time.sleep(0.1)
            if time.time() - start > timeout and timeout > 0:
                return False
        return True
        
    def firmware_put(self, local, remote):
        try: 
            self.sftp.remove(remote)
        except: 
            pass
        print self.sftp.put(local, remote)
        return True