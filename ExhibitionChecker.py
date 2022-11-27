# 檢查是否有新資料
# 不同展館
import ExhibitionMongo

# 檢查展覽資訊是否異動
def CheckExhibition(ExhibitionList):
    db = ExhibitionMongo.InitMongo()
    for Exhibition in ExhibitionList:
        res = db.exhibitions.count_documents({'Title': Exhibition['Title']})  # 数据在mongo中出现的次数

        Exhibition['EndDate']
        EndDate = datetime.strptime(s, '%Y/%m/%d')

        if res == 0:  # 沒有在資料庫中，有新
            ExhibitionMongo.AddExhibition(Exhibition)
        elif False:  # 展覽即將結束
            pass
        else:  # 展覽資訊無異動
            pass
            print('Exhibition existed')
            pass