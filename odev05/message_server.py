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

#Mesaj alici thread implementasyonu
class RecvThread (threading.Thread):
    def __init__(self, name, cSocket, address, logQueue, threadQueue):
        threading.Thread.__init__(self)
        self.name = name
        self.cSocket = cSocket
        self.address = address
        self.lQueue = logQueue
        self.tQueue = threadQueue
        self.nick = ""
    def run(self):
        self.lQueue.put("Starting Recv Thread of Process- " + str(self.name))
        self.flag = False
        while not self.flag:
            queue_message,response = self.parse(self.cSocket.recv(4096))
            self.tQueue.put(response)
            if queue_message != "":
                self.lQueue.put(queue_message)
        self.lQueue.put("Finishing Recv Thread of Process- " + str(self.name))

    def parse(self,msg):
        queue_message = ("")

        if msg[0:3] == "USR":
            if msg[3] == ' ':
                nickname = msg [4:]
                if nickname != "":
                    try :
                        userlist[nickname]
                        response = "REJ " + nickname
                    except KeyError:
                        response = "HEL " + nickname
                        self.nick = nickname
                        user_queue = Queue.Queue(10)
                        userlist[nickname]=user_queue
                else:
                    response = "ERR"
            else:
                response = "ERR"

        elif msg[0:3] == "QUI":
            queue_message = ("QUI",self.nick)
            response = "BYE " + self.nick
            self.flag = True
            try:
                del userlist[self.nick]
            except:
                pass

        elif msg[0:3] == "LSQ":
            users=""
            for key in userlist:
                users += key + ':'
            response = "LSA " + users
            queue_message = ("LSQ",self.nick)

        elif msg[0:3] == "SAY":
            for t in userlist:
                if t != self.nick:
                    userlist[t].put(self.nick+": "+ msg[4:])
            queue_message = ("", self.nick, msg[4:])
            response = "SOK"

        elif msg[0:3] == "TIC":
            response= "TOC"

        elif msg[0:3] == "MSG":
            to_nickname,message  = str.split(msg[4:],':',1)
            try:
                userlist[to_nickname].put(self.nick+": "+ message)
                from_nickname = self.nick
                queue_message = (to_nickname, from_nickname, message)
                response = "MOK"
            except KeyError:
                response = "REJ " + to_nickname
        else:
            response = "ERR"
            queue_message = ("ERR",self.nick)
        return queue_message,response
