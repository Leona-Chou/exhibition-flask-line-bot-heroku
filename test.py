import os
from linebot import LineBotApi
from linebot.models import TextSendMessage
import ExhibitionMongo

# 發送訊息
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
line_bot_api = LineBotApi(channel_access_token)
Users = ExhibitionMongo.GetUserId()
for User in Users:
    line_bot_api.push_message(User["User_Id"], TextSendMessage(text='安安，目前正在測試，如果有跳出任何怪怪的訊息請不要理它~'))
