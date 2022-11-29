# https://github.com/line/line-bot-sdk-python/blob/master/examples/flask-echo/app_with_handler.py

import os
# from dotenv import load_dotenv
import sys
from argparse import ArgumentParser
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, StickerSendMessage
)

import ExhibitionInfo
import ExhibitionMongo

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
# load_dotenv()
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    # 存取user_id
    user_id = event.source.user_id
    ExhibitionMongo.AddUserId(user_id)

    if event.message.text == 'test':  # 測試 text
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text + ' success!'))
        print('test success')
    elif event.message.text == 'picture':  # 測試 picture
        line_bot_api.reply_message(event.reply_token, ImageSendMessage(
            original_content_url='https://mocfile.moc.gov.tw/activitySones/userFiles/CKSMH/JpgFile/01/04758/04758.jpg',
            preview_image_url='https://mocfile.moc.gov.tw/activitySones/userFiles/CKSMH/JpgFile/01/04758/04758.jpg'
        ))
        print('picture get')
    elif event.message.text == 'sticker':  # 測試貼圖
        # 貼圖與代碼對照表 https://developers.line.me/media/messaging-api/messages/sticker_list.pdf
        line_bot_api.reply_message(event.reply_token, StickerSendMessage(package_id=1, sticker_id=2))
        print('sticker get')
    elif event.message.text == '你有什麼功能？':
        # line emoji代碼對照表 https://developers.line.biz/en/docs/messaging-api/emoji-list/#line-emoji-definitions
        line_bot_api.reply_message(event.reply_token, TextSendMessage(
            text='\U0001F449輸入編號來查詢想要的資訊：\n\n1. 中正紀念堂展覽資訊\n\n(其他展覽資訊還在開發中，暫無提供\U0001F62D)'
        ))
        print('功能 get')
    elif event.message.text == '1':
        lists = ExhibitionInfo.GetExihibitionInfo()
        message = ''
        for list in lists:
            message = message\
                      + '展名：' + list['Title'] + '\n' + '開始日：' + list['StartDate'] + '\n' + '結束日：' + list['EndDate'] + '\n'\
                      + '時間：' + list['Time'] + '\n' + '地點：' + list['Location'] + '\n' + list['ExhibitionLink'] + '\n\n'
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='中正紀念堂展覽'+message))
        print('1 get')
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="我不夠聰明，請輸入相關的關鍵詞或者點擊選單我才能理解唷~"))
        print('else')


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)
