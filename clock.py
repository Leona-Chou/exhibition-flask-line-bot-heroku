import sched

import ExhibitionInfo
import ExhibitionChecker


# 防止睡眠
def DoNotSleep():
    ExhibitionList = ExhibitionInfo.GetExihibitionInfo()
    ExhibitionChecker.CheckExhibition(ExhibitionList)

# 防止自動休眠
sched.add_job(DoNotSleep, trigger='interval', id='doNotSleeps_job', seconds=3)
