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
        # print('User_Id success')


# 新增展覽資訊
def AddExhibition(ExhibitionList):
    db = InitMongo()
    for Exhibition in ExhibitionList:
        res = db.exhibitions.count_documents({'Title': Exhibition['Title']})  # 数据在mongo中出现的次数
        if res == 0:  # 沒有在資料庫中，新增
            db.exhibitions.insert_one({
                "Title": Exhibition['Title'],
                "StartDate": Exhibition['StartDate'],
                "EndDate": Exhibition['EndDate'],
                "Time": Exhibition['Time'],
                "Location": Exhibition['Location'],
                "ExhibitionLink": Exhibition['ExhibitionLink'],
                "ImgLink": Exhibition['ImgLink']
            })
            print('Exhibition success')
        else:  # 有在資料庫中，無異動
            print('Exhibition existed')
            pass


# 刪除展覽資訊
def RemoveExhibition(Title):
    db = InitMongo()
    db.exhibitions.delete_one({
        "Title": Title
    })


# 取得展覽資訊
def GetExhibitions():
    db = InitMongo()
    cursor = db.exhibitions.find()
    return list(cursor)


# AddExhibition(ExhibitionList)
# RemoveExhibition("2330")
# print(GetExhibitions())
# AddUserId('U355e7537484ebee1d8b05fa42be9defd')