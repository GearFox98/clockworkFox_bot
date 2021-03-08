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
DB_NAME = "clockworkfox-bot"
PASSWORD = os.environ['MONGO']
CLIENT = "mongodb+srv://clockwork:"+PASSWORD+"@clockworkfox-telegram-b.5eqt8.mongodb.net/clockworkfox-bot?retryWrites=true&w=majority"

cli = pymongo.MongoClient(CLIENT)

def setEventList(gId, content):
  db = cli[DB_NAME]['event']
  try:
    if not content == "nil":
      db.update_one({"_id": gId}, {'$set':{"list": content}})
  except Exception as _error:
    return _error

def getTempList(gId):
  db = cli[DB_NAME]['event']
  try:
    data = db.find({"_id": gId})
    return data[0]['list']
  except Exception as _error:
    print("getTempList Error", _error)
    return list()

def setEventStatus(status, gId):
  db = cli[DB_NAME]['event']
  try:
    if status == True:
      db.update_one({"_id": gId}, {'$set':{"is_active": status, "list": list()}}, True)
    else:
      db.update_one({"_id": gId}, {'$set':{"is_active": status}}, True)
  except Exception as error:
    return error

def getEventStatus(gId):
  db = cli[DB_NAME]['event']
  try:
    status = db.find({"_id": gId})
    return status[0]['is_active']
  except Exception as _error:
    db.insert_one({"_id": gId, "is_active": False})
    return False

def pingMongo(chatId, text):
  db = cli[DB_NAME]['test']
  try:
    db.update_one({"_id": chatId}, {'$set':{"text": text}}, True)
  except Exception as error:
    print(error)
  finally:
    data = db.find({"_id": chatId})
    if data[0]['text'] == 'nil':
      return "Empty"
    else:
      return(data[0]['text'])

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