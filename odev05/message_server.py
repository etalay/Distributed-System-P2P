# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 18:13:51 2015

@author: e-talay
"""

import socket
import threading
import time
import Queue

#Log için gerekli Thread İmplementasyonunu gerceklestirdik.
class LoggerThread (threading.Thread):
    def __init__(self, logQueue, logFileName):
        threading.Thread.__init__(self)
        self.lQueue = logQueue
        self.lFileName = logFileName
    def log(self,message):
        self.fid = open(self.lFileName,"a")
        t = time.time()
        self.fid.write("["+str(t)+"]: " + message)
        self.fid.close()
    def run(self):
        self.log("Starting Logger Process\n")
        while True:
            if not self.lQueue.empty():
                data = self.lQueue.get()
                self.log(str(data)+"\n")
        self.log("Finish Logger Process!\n")
#Mesaj gönderici Thread'i olusturduk.
class SendThread (threading.Thread):
    def __init__(self, name, cSocket, address, threadQueue, logQueue):
        threading.Thread.__init__(self)
        self.name = name
        self.cSocket = cSocket
        self.address = address
        self.lQueue = logQueue
        self.tQueue = threadQueue
        self.nickname = ""
    def run(self):
        self.lQueue.put("Starting Send Thread of Process- " + str(self.name))
        self.flag = False
        while not self.flag:
            if not self.tQueue.empty():
                data = self.tQueue.get()
                self.cSocket.send(data)
                if data[0:3] == "BYE":
                    self.flag = True
                    self.cSocket.close()
                elif data[0:3] == "HEL":
                    self.nickname = data[4:]
            flag = True
            if self.nickname != "":
                try:
                    flag = (userlist[self.nickname]).empty()
                except KeyError:
                    pass
            if not flag:
                self.cSocket.send(userlist[self.nickname].get())
        self.lQueue.put("Exiting Send Thread of Process- " + str(self.name))
