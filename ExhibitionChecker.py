# 檢查是否有新資料
# 不同展館
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
    # Cursor = False
    message1 = ''
    message2 = ''
    for Exhibition in ExhibitionList:
        res = db.exhibitions.count_documents({'Title': Exhibition['Title']})  # 数据在mongo中出现的次数
        interval = (Exhibition['EndDate'] - now).days + 1

        if res == 0:  # 沒有在資料庫中，有新展覽
            ExhibitionMongo.AddExhibition(Exhibition)

        elif interval == 7:  # 結束前7日提醒
            message1 = message1 \
                       + '展名：' + Exhibition['Title'] \
                       + '\n開始日：' + datetime.strftime(Exhibition['StartDate'], '%Y/%m/%d') \
                       + '\n結束日：' + datetime.strftime(Exhibition['EndDate'], '%Y/%m/%d') \
                       + '\n時間：' + Exhibition['Time'] \
                       + '\n地點：' + Exhibition['Location'] + '\n' \
                       + Exhibition['ExhibitionLink'] + '\n\n'
            print('will be end in 7 days')
            pass

        elif interval == 3:  # 結束前3日提醒
            message2 = message2\
                      + '展名：' + Exhibition['Title'] \
                      + '\n開始日：' + datetime.strftime(Exhibition['StartDate'], '%Y/%m/%d') \
                      + '\n結束日：' + datetime.strftime(Exhibition['EndDate'], '%Y/%m/%d') \
                      + '\n時間：' + Exhibition['Time'] \
                      + '\n地點：' + Exhibition['Location'] \
                      + Exhibition['ExhibitionLink']
            print('will be end in 3 days')
            pass

        elif interval == 0:  # 展覽結束，將資料存入展覽回顧(historyex)，並從當前展覽(exhibitions)刪除
            print('exhibition end')
            pass

        else:  # 展覽資訊無異動
            print('exhibition info not change')
            pass

    # 傳送訊息給用戶
    for User in Users:
        if message1 != '':
            line_bot_api.push_message(User["User_Id"], TextSendMessage(text='以下展覽還有7天將結束：\n\n' + message1))
        if message2 != '':
            line_bot_api.push_message(User["User_Id"], TextSendMessage(text='以下展覽還有3天將結束：\n\n' + message2))


# 防止睡眠
def DoNotSleep():
    url = "https://leonalinebot.herokuapp.com/"
    r = requests.get(url)
    print('clock')

'''
# 取得現在時間
now_time = datetime.datetime.now();
# 設定預計執行的時間
next_year = now_time.date().year
next_month = now_time.date().month
next_day = now_time.date().day

next_time = datetime.datetime.strptime(str(next_year)+'-'+str(next_month)+'-'+str(next_day)+' 00:00:01', '%Y-%m-%d %H:%M:%S');
# 計算預定執行的時間與現在的時間間隔，並換算為秒數。
timer_start_time = (next_time - now_time).total_seconds()

# 初始化 schedule
schedule = sched.scheduler(time.time, time.sleep)
# 設定 schedule 及執行
schedule.enter(timer_start_time, 0, CheckExhibition,())
schedule.run()
'''

# 開始建立排程任務
sched = BlockingScheduler()

# 每日執行
# sched.add_job(CheckExhibition, trigger='interval', args=(ExhibitionList,), id='CheckExhibition_job', seconds=20)

# 防止自動休眠
sched.add_job(DoNotSleep, trigger='interval', id='DoNotSleeps_job', seconds=20)

# 啟動排程
sched.start()
