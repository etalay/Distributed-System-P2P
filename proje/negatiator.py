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
