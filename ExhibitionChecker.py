import os
from linebot import LineBotApi
from linebot.models import TextSendMessage
from apscheduler.schedulers.blocking import BlockingScheduler
import requests
from datetime import datetime
import ExhibitionInfo
import ExhibitionMongo

ExhibitionList = ExhibitionInfo.GetExihibitionInfo()
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
line_bot_api = LineBotApi(channel_access_token)
Users = ExhibitionMongo.GetUserId()


# 檢查展覽資訊是否異動
def CheckExhibition(ExhibitionList):

    db = ExhibitionMongo.InitMongo()
    now = datetime.now()
    GetExhibition = ExhibitionMongo.GetExhibitions()
    messageAdd = ''
    message1 = ''

    for Exhibition in ExhibitionList:
        res = db.exhibitions.count_documents({'Title': Exhibition['Title']})  # 数据在mongo中出现的次数
        interval = (Exhibition['EndDate'] - now).days + 1

        if res == 0:  # 沒有在資料庫中，有新展覽
            ExhibitionMongo.AddExhibition(Exhibition)
            messageAdd += '展名：' + Exhibition['Title'] \
                       + '\n開始日：' + datetime.strftime(Exhibition['StartDate'], '%Y/%m/%d') \
                       + '\n結束日：' + datetime.strftime(Exhibition['EndDate'], '%Y/%m/%d') \
                       + '\n時間：' + Exhibition['Time'] \
                       + '\n地點：' + Exhibition['Location'] + '\n' \
                       + Exhibition['ExhibitionLink'] + '\n\n'

        elif interval == 7:  # 結束前7日提醒
            message1 += '展名：' + Exhibition['Title'] \
                     + '\n開始日：' + datetime.strftime(Exhibition['StartDate'], '%Y/%m/%d') \
                     + '\n結束日：' + datetime.strftime(Exhibition['EndDate'], '%Y/%m/%d') \
                     + '\n時間：' + Exhibition['Time'] \
                     + '\n地點：' + Exhibition['Location'] + '\n' \
                     + Exhibition['ExhibitionLink'] + '\n\n'
            print('Will be end in 7 days')

    # 展覽結束，將資料存入展覽回顧(histories)，並從當前展覽(exhibitions)刪除
    for Exhibitionn in GetExhibition:
        if ((Exhibitionn['EndDate'] - now).days + 1) <= 0:
            ExhibitionMongo.AddHistories(Exhibitionn)  # 存入 histories
            ExhibitionMongo.RemoveExhibition(Exhibitionn['Title'])  # 從 exhibitions 刪除
            print('exhibition end')
        else:
            pass

    # 傳送訊息給用戶
    for User in Users:
        if messageAdd != '' or message1 != '':  # 新增展覽
            if messageAdd != '':
                line_bot_api.push_message(User["User_Id"], TextSendMessage(text='更新以下新的展覽：\n\n' + messageAdd))
            if message1 != '':  # 還有7天
                line_bot_api.push_message(User["User_Id"], TextSendMessage(text='以下展覽還有7天將結束：\n\n' + message1))
        else:
            print('Nothing changed')


# 防止睡眠
def DoNotSleep():
    url = "https://leonalinebot.herokuapp.com/callback"
    r = requests.get(url)
    print('DoNotSleep')



# 開始建立排程任務
sched = BlockingScheduler(timezone="Asia/Taipei")

# 每日執行
sched.add_job(CheckExhibition, args=(ExhibitionList,), trigger='cron', id='CheckExhibition_job', hour=10, minute=30)

# 防止自動休眠
sched.add_job(DoNotSleep, trigger='interval', id='DoNotSleeps_job', minutes=20)

# 啟動排程
sched.start()
