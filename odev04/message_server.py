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
            
            
            
            #istemci ile beraber calısacak olan socketThread implementasyonunu gerceklestirdik.
class socketThread(threading.Thread):
    def __init__(self, threadID, clientSocket, clientAddr):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.clientSocket = clientSocket
        self.clientAddr = clientAddr
    def run(self):
        threadd = timeClass(self.clientSocket)
        threadd.start()
        print "Starting Thread-" + str(self.threadID)
        while True:
            if self.clientSocket.recv(4096)=="STOP":
                self.clientSocket.close()
                break
            else:
                print "Peki" + str(self.clientSocket.getpeername())
        print "Finishing Thread-" + str(self.threadID)
        threadd.join()


#thread numaralarını saymasi icin bir sayac olusturduk.
threadCounter = 0

#socket olusturduktan sonra host ve port adreslerini girdik ve bu adresle iletisim halinde olmasi icin bir listener ekledik
s = socket.socket()
host = "localhost"
port = 12346
s.bind((host,port))
s.listen(5)
threads = []

#Surekli bir baglanti olusturarak İstemci'nin her zaman cevap alabilecegi bir döngü gerceklestirdik. 
while True:
    print "Waiting for connection"
    c,addr = s.accept()
    print "A new connection from ",addr
    threadCounter += 1
    thread = socketThread(threadCounter,c,addr)
    threads.append(thread)
    thread.start()

for t in threads:
    t.join()
