# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 21:04:15 2021
FileSystem Handler
"""

import pymongo
from bson.objectid import ObjectId
import os.path as ph
import os

SYS = "../sys/"
LOG = "../logs/log_"
IS_EVENT = False
DB_NAME = "clockworkfox-bot"
CLIENT = os.environ['MONGO']

cli = pymongo.MongoClient(CLIENT)

def writeEventList(gId, content):
  collection = "event-content"
  db = cli[DB_NAME][collection]
  try:
    db.insert_one({"_id": gId, "list": content})
  except Exception as error:
    if type(error) == pymongo.errors.DuplicateKeyError:
      db.update_one({"_id": gId}, {"list": content})

def getEventList(gId):
  collection = "event-content"
  db = cli[DB_NAME][collection]
  return db.find({"_id": gId}, {"_id": False})

def setEventStatus(status, gId):
  collection = "event"
  db = cli[DB_NAME][collection]
  try:
    db.update_one({"_id": gId}, {"is_active": status}, True)
  except Exception as error:
    return error

def getEventStatus(gId):
  collection = "event"
  db = cli[DB_NAME][collection]
  try:
    return db.find({"_id": gId}, {"_id": False})
  except Exception as _error:
    db.insert_one({"_id": gId, "is_active": False})
    return False


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
