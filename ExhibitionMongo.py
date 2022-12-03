import os
from dotenv import load_dotenv
from pymongo import MongoClient
import ExhibitionInfo

ExhibitionList = ExhibitionInfo.GetExihibitionInfo()
load_dotenv()

MONGODB_URL = os.getenv('MONGODB_URL', None)
DATABASE_NAME = 'ExhibitionLineBot'
COLLECTION_NAME = 'exhibition'


# 初始化
def InitMongo():
    client = MongoClient(MONGODB_URL, ssl=True, ssl_cert_reqs='CERT_NONE')
    db = client[DATABASE_NAME]
    return db


# 新增用戶ID
def AddUserId(UserId):
    db = InitMongo()
    res = db.users.count_documents({'User_Id': UserId})  # 数据在mongo中出现的次数

    if res == 0:
        db.users.insert_one({
            "User_Id": UserId
        })
        print('User_Id success')


# 取得用戶ID
def GetUserId():
    db = InitMongo()
    cursor = db.users.find()
    print('get exhibition info')
    return list(cursor)


# 新增展覽資訊
def AddExhibition(ExhibitionList):
    db = InitMongo()
    db.exhibitions.insert_one({
        "Title": ExhibitionList['Title'],
        "StartDate": ExhibitionList['StartDate'],
        "EndDate": ExhibitionList['EndDate'],
        "Time": ExhibitionList['Time'],
        "Location": ExhibitionList['Location'],
        "ExhibitionLink": ExhibitionList['ExhibitionLink'],
        "ImgLink": ExhibitionList['ImgLink']
    })
    print('add success')


# 刪除展覽資訊
def RemoveExhibition(Title):
    db = InitMongo()
    db.exhibitions.delete_one({
        "Title": Title
    })
    print('remove success')


# 取得展覽資訊
def GetExhibitions():
    db = InitMongo()
    cursor = db.exhibitions.find()
    print('get exhibition info')
    return list(cursor)


# 將展覽資訊存入 histories
def AddHistories(ExhibitionList):
    db = InitMongo()
    db.exhibitions.insert_one({
        "Title": ExhibitionList['Title'],
        "StartDate": ExhibitionList['StartDate'],
        "EndDate": ExhibitionList['EndDate'],
        "Time": ExhibitionList['Time'],
        "Location": ExhibitionList['Location'],
        "ExhibitionLink": ExhibitionList['ExhibitionLink'],
        "ImgLink": ExhibitionList['ImgLink']
    })
