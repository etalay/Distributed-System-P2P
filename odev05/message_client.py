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
#Yazma thread implmentasyonunu gerceklestirdik.
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
#Socket'i olusturduk
s = socket.socket()
#Server icin gerekli host ve port bilgilerini girdik.
host = "178.233.19.205"
port = 12345
#Baglantiyi gerceklestirdik.
s.connect((host,port))
#Thread'leri olusturup baslattik.
rThread = readThread(s)
rThread.start()

wThread = writeThread(s)
wThread.start()

rThread.join()
wThread.join()
