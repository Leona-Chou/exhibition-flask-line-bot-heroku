# 檢查是否有新資料
# 不同展館
import ExhibitionInfo
import ExhibitionMongo
import sched
from datetime import datetime
import time

ExhibitionList = ExhibitionInfo.GetExihibitionInfo()

# 檢查展覽資訊是否異動
def CheckExhibition(ExhibitionList):
    db = ExhibitionMongo.InitMongo()
    for Exhibition in ExhibitionList:
        res = db.exhibitions.count_documents({'Title': Exhibition['Title']})  # 数据在mongo中出现的次数
        if res == 0:  # 沒有在資料庫中，有新展覽
            ExhibitionMongo.AddExhibition(Exhibition)
        elif False:  # 展覽結束，將資料存入展覽回顧(historyex)，並從當前展覽(exhibitions)刪除
            print('exihibition end')
            pass
        elif False:  # 展覽即將結束(結束前三日提醒)
            print('will be end')
            pass
        else:  # 展覽資訊無異動
            print('Exhibition existed')
            pass


'''
# 取得現在時間
now_time = datetime.datetime.now();
# 設定預計執行的時間
next_year = now_time.date().year
next_month = now_time.date().month
next_day = now_time.date().day

next_time = datetime.datetime.strptime(str(next_year)+'-'+str(next_month)+'-'+str(next_day)+' 00:00:00', '%Y-%m-%d %H:%M:%S');
# 計算預定執行的時間與現在的時間間隔，並換算為秒數。
timer_start_time = (next_time - now_time).total_seconds()

# 初始化 schedule
schedule = sched.scheduler(time.time, time.sleep)
# 設定 schedule 及執行
schedule.enter(timer_start_time, 0, CheckExhibition,())
schedule.run()
'''