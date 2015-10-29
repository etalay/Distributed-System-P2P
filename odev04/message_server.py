# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 15:39:03 2015

@author: e-talay
"""


import threading
import random
import socket
import time
from datetime import datetime

#Bilgisayardan anlýk olarak saati almamýza yarayan timeClass implementasyonunu gerceklestirdik.
class timeClass (threading.Thread):
    def __init__(self,clientSocket):
        threading.Thread.__init__(self)
        self.clientSocket = clientSocket
    def run(self):
        while True:
            try:
                self.clientSocket.send("Merhaba, Saat "+datetime.now().strftime('%H:%M:%S'))
            except:
                break
            time.sleep(random.randint(20,30))