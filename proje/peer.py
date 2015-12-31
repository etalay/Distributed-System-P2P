# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 22:18:11 2015
@author: e-talay
"""
#!/usr/bin/env python


import Queue
import time
import sys
import copy
import threading
import socket


# peer host adresi
hostName = "192.168.1.38"
# peer port numarasi
portNumber = 12347
# baglanti listesi
CONNECT_POINT_LIST = {}
# tüm liste icin bekleme 
TEST_WAIT_TIME = 30
# zamanasimi 
TEMP_SOCK_TIMEOUT = 10
# Chunk Size(bytes)
CHUNK_SIZE = 4096
# Ratio Constant 
RAITO_CST = 0.8
# Arabulucu host adresi
NEGO_HOST = "192.168.1.35"
# Arabulucu port adresi
NEGO_PORT = 12345
