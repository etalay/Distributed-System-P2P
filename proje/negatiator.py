# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 21:13:51 2015
@author: e-talay
"""
#!/usr/bin/env python

import time
import copy
import threading
import socket
import Queue

#Baglanti listesi
CONNECT_POINT_LIST = {}

# Arabulucu port numarasi
portNumber = 12345

# Soket zamanasimi 
TEMP_SOCK_TIMEOUT = 10

# tum liste icin bekleme
TEST_WAIT_TIME = 10
