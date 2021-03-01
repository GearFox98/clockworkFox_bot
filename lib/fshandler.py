# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 21:04:15 2021
FileSystem Handler
"""

import pymongo
import os.path as ph
import os

SYS = "../sys/"
LOG = "../logs/log_"


def getToken():
    return os.environ['TOKEN']

def loadConfig(gId):
    x = SYS + str(gId) + "_lang.conf"
    if ph.exists(SYS + str(gId) + "_lang.conf"):
        fileStream = open(x, 'rb')
        return fileStream.read()
    else:
        return 'en'
    fileStream.Close()

def saveConfig(gId, conf):
    x = SYS + str(gId) + "_lang.conf"
    if conf == 'en':
        x = SYS + str(gId) + "_lang.conf"
        fileStream = open(x, 'wb')
        fileStream.write(conf)
    else:
        if ph.exists(x):
            os.remove(x)
    fileStream.Close()

def writeConts(conts, gId):
  x = SYS + "clockworkEvent_" + str(gId)
  if ph.exists(x):
    os.remove(x)
  with open(x, 'w') as fileStream:
    for y in conts:
      fileStream.write(y)
  fileStream.Close()

def readConts(gId):
  x = SYS + "clockworkEvent_" + str(gId)
  if ph.exists(x):
    with open(x, 'r') as fileStream:
      y = fileStream.read().splitlines()
    fileStream.Close()
    return y
  else:
    return list()
