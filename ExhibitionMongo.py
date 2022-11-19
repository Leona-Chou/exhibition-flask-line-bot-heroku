import os

from dotenv import load_dotenv
from pymongo import MongoClient
import datetime
load_dotenv()

MONGODB_URL = os.getenv('MONGODB_URL')
DATABASE_NAME = 'ExhibitionLineBot'
COLLECTION_NAME = 'Exhibition'

def InitMongo():
    client = MongoClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    return db

def AddExhibition(name, price, operator="less_than"):
    db = InitMongo()
    db.stocks.insert_one({
        "name": name,
        "price": float(price),
        "operator": operator
    })

def RemoveStock(name):
    db = InitMongo()
    db.stocks.delete_one({
        "name": name
    })

def GetStocks():
    db = InitMongo()
    cursor = db.stocks.find()
    return list(cursor)


AddExhibition("2330", 705, 'less_than')
# AddExhibition("2330", 635, 'greater_than')
# RemoveStock("2330")
# print(GetStocks())
