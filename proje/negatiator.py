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

