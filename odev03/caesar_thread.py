# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 15:55:37 2015

@author: e-talay
"""

import string


#Kriptolama icin kullandigimiz algoritma.
def caesar(substring, shift_number, decode = False):
   if decode: shift_number = 26 - shift_number
   return substring.translate(
       string.maketrans(
           string.ascii_uppercase + string.ascii_lowercase,
           string.ascii_uppercase[shift_number:] + string.ascii_uppercase[:shift_number] +
           string.ascii_lowercase[shift_number:] + string.ascii_lowercase[:shift_number]
           )
       )

