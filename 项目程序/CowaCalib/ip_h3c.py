# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import requests, json, re, urllib2, time

import pytesser
from PIL import Image

url = lambda page: 'http://192.168.1.1/' + page
class H3CRouter:
    sessionid = 'ABCDEFGH'
    header = {  'Host': '192.168.1.1', 
                'Connection': 'keep-alive',
                'Content-Length': '75', 
                'Cache-Control': 'max-age=0', 
                'Origin': 'http://192.168.1.1', 
                'Upgrade-Insecure-Requests': '1', 
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Mobile Safari/537.36', 
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Referer': 'http://192.168.1.1/userLogin.asp', 
                'Accept-Encoding': 'gzip, deflate', 
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7'}
    def __loginpost(self, loginData):
        cont = requests.post(url('userLogin.asp'), data = loginData, headers = self.header)
        if 'sessionid' in cont.content:
            id = cont.content.split('sessionid="', 2)[1]
            id = id.split('"', 2)[0]
            return id
        else:
            return 'ABCDEFGH'
    def __getvldcode(self):
        cont = requests.get(url('vld.bmp?0.30659009179925256'), data = '0.30659009179925256', headers=self.header)
        f = open('tmp.bmp', 'wb').write(cont.content)
        img = Image.open('tmp.bmp').resize((72,18),Image.ANTIALIAS)
        vcode = pytesser.image_to_string(img).strip()
        return vcode
    def login(self):
        loginData = {'save2Cookie':'', 'vldcode':'', 'account':'admin', 'password':'admin', 'btnSubmit':'+%B5%C7%C2%BC+'}
        id = self.__loginpost(loginData)
        if id == 'ABCDEFGH':
            loginData['vldcode'] = self.__getvldcode()
            id = self.__loginpost(loginData)
            print id, loginData['vldcode']
            
        self.sessionid = id
    def logout(self):
        cont=requests.post(url('goform/aspForm'), cookies={'JSESSIONID':self.sessionid})
        cont=requests.get(url('login.htm'), cookies={'JSESSIONID':self.sessionid})
    def listHost(self):
        #opener = urllib2.build_opener()
        #opener.addheaders.append(('Cookie','JSESSIONID='+id))
        #f = opener.open('http://192.168.1.1/dhcpd_client.asp#bigTitle', timeout=60)
        #print f.read()
        while self.sessionid == 'ABCDEFGH':
            self.login()
            if self.sessionid == 'ABCDEFGH':
                print 'try login filed, relogin...'
                time.sleep(5)
            else:
                print 'loading success'
        dhcp = []       
        client = []
        cont = requests.post(url('dhcpd_client_list.asp'), cookies={'JSESSIONID':self.sessionid})
        if 'new Array(' in cont.content:
            cont = cont.content.split('new Array(', 2)[1]
            cont = cont.split(');', 2)[0].replace(';lanbr1', '')
            cont = '[' + cont + ']'
            cont = eval(cont.upper())
            #for i in cont:
            #    print i
            dhcp = cont
        #print dhcp
        cont = requests.post(url('wlan_ap_client_list.asp'), cookies={'JSESSIONID':self.sessionid})    
        if 'new Array(' in cont.content:
            cont = cont.content.split('new Array(', 2)[1]
            cont = cont.split(');', 2)[0].replace(';lanbr1', '')
            cont = '[' + cont + ']'
            cont = eval(cont)
            #print cont
            for mac in cont:
                mac = mac.split(';')[1].upper()
                #print mac
                for host in dhcp:
                    #print host.find(mac),
                    if host.find(mac) >= 0:
                        client.append(host.strip())
                #print ' '
        return client     
if __name__ == '__main__':
    h3c = H3CRouter()
    while 1:
        print'##########################'
        for i in h3c.listHost():
            print i
        time.sleep(1)