# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 21:04:15 2021
FileSystem Handler
"""

import logging
import dataparser.parser as parser
import os.path as ph
import os

SYS = "sys"
LOG = "logs/log_"

# Set logger    
logging.basicConfig(
  level = logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s,"
)
LOGGER = logging.getLogger()

#Database
#Event!
def setEventList(gId, content):
  try:
    if not content == "nil":
      parser.update_file(f"{SYS}/event/{gId}.json", {'id': gId, 'list': content})
  except Exception as _error:
    return _error

def getTempList(gId):
  try:
    data = parser.get_data(f"{SYS}/event/{gId}.json", ("list"), True)['list']
    return data
  except Exception as _error:
    print("getTempList Error", _error)
    return list()

def setEventStatus(status, gId):
  try:
    if status == True:
      parser.update_file(f"{SYS}/event/{gId}.json", {'id': gId, 'is_active': status})
    else:
      parser.delete_data(f"{SYS}/event/{gId}.json")
  except Exception as error:
    LOGGER.error(error)

def getEventStatus(gId):
  try:
    return parser.get_data(f"{SYS}/event/{gId}.json", ("is_active"), True)['is_active']
  except Exception as _error:
    return False

#Raffle!
def setRaffleMax(gId, author, part):
  try:
    parser.update_file(f"{SYS}/raffle/{gId}.json", {'id': gId, 'is_raffle': True, 'author': author, 'max': part, 'cont': list()})
    print(author)
  except Exception as _error:
    return _error

def setRaffle(gId, cont):
  try:
    parser.update_file(f"{SYS}/raffle/{gId}.json", {'cont': cont})
  except Exception as _error:
    return _error

def getRaffleCont(gId):
  return parser.get_data(f"{SYS}/raffle/{gId}.json", ("cont"), True)['cont']

def getRaffle(gId):  
  dataSet = parser.get_data(f"{SYS}/raffle/{gId}.json", ('max', 'cont'), True)

  parser.delete_data(f"{SYS}/raffle/{gId}.json")
  return dataSet

def getIsRaffle(gId):
  try:
    data = parser.get_data(f"{SYS}/raffle/{gId}.json", ('is_raffle'), True)['is_raffle']
    return data
  except:
    return False

#Cancel
def cancel(gId, type_event, *user):
  if type_event == "event":
    setEventStatus(False, gId)
  elif type_event == "raffle":
    author = parser.get_data(f"{SYS}/raffle/{gId}.json", (), True)['author']
    if user[0] == author:
      parser.delete_data(f"{SYS}/raffle/{gId}.json")
      return True
    else:
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