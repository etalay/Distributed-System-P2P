# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 15:39:03 2015

@author: e-talay
"""
import threading
import socket

#Okuma thread'i implementasyonu
class readThread (threading.Thread):
    def __init__(self,clientSocket):
        threading.Thread.__init__(self)
        self.clientSocket = clientSocket
    def run(self):
        global boolean
        print "Reading Thread is starting"
        while not boolean:
            print(self.clientSocket.recv(4096))