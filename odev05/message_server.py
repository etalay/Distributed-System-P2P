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
