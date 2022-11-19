import os

from dotenv import load_dotenv
from pymongo import MongoClient
import ExhibitionInfo
ExhibitionList = ExhibitionInfo.GetExihibitionInfo()
load_dotenv()

MONGODB_URL = os.getenv('MONGODB_URL')
DATABASE_NAME = 'ExhibitionLineBot'
COLLECTION_NAME = 'exhibition'

def InitMongo():
    client = MongoClient(MONGODB_URL, ssl=True, ssl_cert_reqs='CERT_NONE')
    db = client[DATABASE_NAME]
    return db

def AddUserId(UserId):
    db = InitMongo()
    db.user.insert_one({
        "User_Id": UserId
    })

def AddExhibition(ExhibitionList):
    db = InitMongo()
    for Exhibition in ExhibitionList:
        res = db.exhibitions.count_documents({'Title': Exhibition['Title']})  # 数据在mongo中出现的次数
        if res == 0:  # 有新增的展覽資訊
            db.exhibitions.insert_one({
                "Title": Exhibition['Title'],
                "StartDate": Exhibition['StartDate'],
                "EndDate": Exhibition['EndDate'],
                "Time": Exhibition['Time'],
                "Location": Exhibition['Location'],
                "ExhibitionLink": Exhibition['ExhibitionLink'],
                "ImgLink": Exhibition['ImgLink']
            })
            print('資料庫更新')  # TODO: 更新資料庫
        elif False:  # 有展覽結束
            # TODO: 將展覽資訊添加到展覽回顧資料表, 並從當前展覽資料表刪除
            pass
        else:  # 展覽資訊無異動, 無需做任何動作
            print('existed')

def RemoveExhibition(Title):
    db = InitMongo()
    db.exhibitions.delete_one({
        "Title": Title
    })

def GetExhibitions():
    db = InitMongo()
    cursor = db.exhibitions.find()
    return list(cursor)


# AddExhibition(ExhibitionList)
# RemoveExhibition("2330")
# print(GetExhibitions())
