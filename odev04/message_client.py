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
            
            #Yazma thread'i implementasyonu
class writeThread (threading.Thread):
    def __init__(self,clientSocket):
        threading.Thread.__init__(self)
        self.clientSocket = clientSocket
    def run(self):
        global boolean
        print "\nWriting Thread is starting"
        while not boolean:
            char = raw_input("")
            if char=="STOP":            #Kullanici "STOP" komutu girince program sonlanicak.
                self.clientSocket.send(char)
                boolean = True
                self.clientSocket.close()
            else:
                self.clientSocket.send(char)
                
                
boolean = False
#Socket'i tanımlıyıp host ve port adreslerini belirtiyoruz.
s = socket.socket()
host = "localhost"
port = 12346
s.connect((host,port))

print "hey"+str(s.getpeername())
