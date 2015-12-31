# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 21:13:51 2015
@author: e-talay
"""
#!/usr/bin/env python

import time
import copy
import threading
import socket
import Queue

#Baglanti listesi
CONNECT_POINT_LIST = {}

# Arabulucu port numarasi
portNumber = 12345

# Soket zamanasimi 
TEMP_SOCK_TIMEOUT = 10

# tum liste icin bekleme
TEST_WAIT_TIME = 10

# peer client'larını test et
class clientThread (threading.Thread):
    def __init__(self,testQ):
        threading.Thread.__init__(self)
        self.testQ = testQ
    def run(self):
        tlThread = testlistThread()
        tlThread.start()
        while True:
            if not self.testQ.empty():
                peer = self.testQ.get()
                tThread = testThread(peer)
                tThread.start()

#her TEST_WAIT_TIME sonunda listeyi test et
class testlistThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        while True:
            time.sleep(TEST_WAIT_TIME)
            for point in CONNECT_POINT_LIST:
                tThread = testThread(point)
                tThread.start()
            print CONNECT_POINT_LIST


# Test thread
class testThread (threading.Thread):
    def __init__(self,point):
        threading.Thread.__init__(self)
        self.point = point
    def run(self):
        global CONNECT_POINT_LIST
        temp = socket.socket()
        temp.settimeout(TEMP_SOCK_TIMEOUT)
        COPY_LIST = copy.deepcopy(CONNECT_POINT_LIST)
        try:
            temp.connect((COPY_LIST[self.point][0],int(COPY_LIST[self.point][1])))
            temp.send("HELLO")
            try:
                response = temp.recv(4096)
                if response[:5] != "SALUT":
                    temp.send("CMDER")
                    temp.close()
                    if self.point in COPY_LIST:
                        del COPY_LIST[self.point]
                else:
                    if COPY_LIST[self.point][4]=="W":
                        COPY_LIST[self.point][2] = str(time.time())
                        COPY_LIST[self.point][4] = "S"
                        COPY_LIST[self.point][3] = response[6:]
                    elif COPY_LIST[self.point][4]=="S":
                        COPY_LIST[self.point][2] = str(time.time())
                    temp.send("CLOSE")
                    temp.close()
            except socket.timeout:
                del COPY_LIST[self.point]
                temp.close()
        except:
            del COPY_LIST[self.point]
            temp.close()
        CONNECT_POINT_LIST = copy.deepcopy(COPY_LIST)

# Arabulucunun server tarafı
class serverThread (threading.Thread):
    def __init__(self,testQ):
        threading.Thread.__init__(self)
        self.testQ = testQ
    def run(self):
        s = socket.socket()
        s.bind(("",portNumber))
        s.listen(5)
        while True:
            c,addr = s.accept()
            print "A new connection from ",addr
            thread = peerThread(c,addr,self.testQ)
            thread.start()

# peer'lari yonetmek icin
class peerThread (threading.Thread):
    def __init__(self,c,addr,testQ):
        threading.Thread.__init__(self)
        self.socket = c
        self.addr = addr
        self.testQ = testQ
        self.flagAuth = False
        self.flagOK = True
    def run(self):
        global CONNECT_POINT_LIST
        self.socket.settimeout(TEMP_SOCK_TIMEOUT*2)
        for i in range(2):
            if self.flagOK:
                try:
                    message = self.socket.recv(4096)
                    self.parser(message)
                except socket.timeout:
                    self.socket.close()
                    self.flagOK = False

    def parser(self,message):
        if message[:5] == "REGME":
            try:
                host,port = str.split(message[6:],':',1)
            except:
                self.socket.send("REGER")
                self.flagOK = False
            if self.flagOK:
                if host+port in CONNECT_POINT_LIST:
                    if CONNECT_POINT_LIST[host+port][4]=="S":
                        CONNECT_POINT_LIST[host+port][2] = str(time.time())
                        self.socket.send("REGOK "+str(CONNECT_POINT_LIST[host+port][2]))
                        self.flagOK = True
                        self.flagAuth = True

                else:
                    self.socket.send("REGWA")
                    self.flagOK = False
                    self.socket.close()
                    l=[]
                    l.append(host)
                    l.append(port)
                    l.append(str(time.time()))
                    l.append(" ")
                    l.append("W")
                    CONNECT_POINT_LIST[host+port]=l
                    self.testQ.put(host+port)

        elif message[:5] == "GETNL":
            if self.flagAuth:
                self.socket.send("NLIST BEGIN")
                for point in CONNECT_POINT_LIST:
                    self.socket.send(CONNECT_POINT_LIST[point][0]+":"+CONNECT_POINT_LIST[point][1]+":"+CONNECT_POINT_LIST[point][2]+":"+CONNECT_POINT_LIST[point][3]+"\n")
                self.socket.send("NLIST END")
            else:
                self.socket.send("REGER")
                self.flagOK = False
                self.socket.close()

        elif message == "HELLO":
            self.socket.send("SALUT N")
            self.flagOK = False

        else:
            self.socket.send("CMDER")
            self.flagOK = False
            self.socket.close()

testQ = Queue.Queue(10)

cThread = clientThread(testQ)
cThread.start()

sThread = serverThread(testQ)
sThread.start()
