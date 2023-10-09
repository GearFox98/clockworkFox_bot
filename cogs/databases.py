# -*- coding: utf-8 -*-

import logging
import pymongo
import os.path as ph
import os

SYS = "sys"
LOG = "logs/log_"
DB_NAME = "clockworkfox-bot"
PASSWORD = os.getenv('MONGO')
CLIENT = f"mongodb+srv://clockwork:{PASSWORD}@clockworkfox-telegram-b.5eqt8.mongodb.net/clockworkfox-bot?retryWrites=true&w=majority"

cli = pymongo.MongoClient(CLIENT)

# Set logger    
logging.basicConfig(
  level = logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s,"
)
LOGGER = logging.getLogger()

#Database
#Event!
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
            #db.update_one({"_id": gId}, {'$set':{"is_active": status}}, True)
            db.delete_one({"_id": gId})
    except Exception as error:
        return error

def getEventStatus(gId):
    db = cli[DB_NAME]['event']
    try:
        status = db.find({"_id": gId})
        return status[0]['is_active']
    except Exception as _error:
        return False

#Raffle!
def setRaffleMax(gId, author, part):
    db = cli[DB_NAME]['raffle']
    try:
        db.update_one({"_id": gId}, {'$set': {'is_raffle': True, 'author': author, 'max': part, 'cont': list()}}, True)
    except Exception as _error:
        return _error

def setRaffle(gId, cont):
    db = cli[DB_NAME]['raffle']
    try:
        db.update_one({'_id': gId}, {'$set': {'cont': cont}})
    except Exception as _error:
        return _error

def getAuthor(gId):
    db = cli[DB_NAME]['raffle']
    try:
        author = db.find({"_id": gId})[0]['author']
        return author
    except Exception as error:
        LOGGER.error(error)

def getRaffleCont(gId):
    db = cli[DB_NAME]['raffle']
    status = db.find({"_id": gId})
    return status[0]['cont']

def getRaffle(gId):
    db = cli[DB_NAME]['raffle']
    data = db.find({'_id': gId})
    dataSet = {
        'max': data[0]['max'],
        'cont': data[0]['cont']
    }
  
    db.delete_one({'_id': gId})
    return dataSet

def getIsRaffle(gId):
    db = cli[DB_NAME]['raffle']
    try:
        data = db.find({'_id': gId})
        return data[0]['is_raffle']
    except:
        return False

#Cancel
def cancelRaff(gId, user):
    db = cli[DB_NAME]['raffle']
    author = db.find({"_id": gId})[0]['author']
    if user == author:
        db.delete_one({'_id': gId})
        return True
    else:
        return False

def cancelEv(gId):
    try:
        db = cli[DB_NAME]['event']
        db.delete_one({"_id": gId})
    except Exception as error:
        return error

def loadConfig(gId):
    x = SYS + str(gId) + "_lang.conf"
    if ph.exists(SYS + str(gId) + "_lang.conf"):
        fileStream = open(x, 'rb')
        return fileStream.read()
    else:
        return 'en'
    fileStream.Close()