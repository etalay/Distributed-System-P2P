# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 18:13:51 2015

@author: e-talay
"""
import socket
import threading

#Okuma thread implmentasyonunu gerceklestirdik.
class readThread (threading.Thread):
    def __init__(self,clientSocket):
        threading.Thread.__init__(self)
        self.clientSocket = clientSocket
        self.flag = False
    def run(self):
        print "Starting readThread "
        while not self.flag:
            data = self.clientSocket.recv(4096)
            if data[0:3]=="BYE":
                self.flag = True
                self.clientSocket.close()
            print data

class writeThread (threading.Thread):
    def __init__(self,clientSocket):
        threading.Thread.__init__(self)
        self.clientSocket = clientSocket
        self.flag = False
    def run(self):
        print "Starting writingThread"
        while not self.flag:
            var = raw_input("")
            self.clientSocket.send(var)
            if var[0:3] == "QUI":
                self.clientSocket.close()
                self.flag = True
