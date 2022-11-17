# https://github.com/line/line-bot-sdk-python/blob/master/examples/flask-echo/app_with_handler.py

import os
from dotenv import load_dotenv
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
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage,
)

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
load_dotenv()
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
    user_id = event.source.user_id
    print('user_id:' + user_id)

    # line_bot_api.reply_message(event.reply_token, TextSendMessage(text="reply: "+event.message.text))
    if event.message.text == 'test':  # 測試
        print('test success')
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text + ' success!'))
    elif event.message.text == 'picture':
        print('picture get')
        line_bot_api.reply_message(event.reply_token, ImageSendMessage(
            original_content_url='https://images.builderservices.io/s/cdn/v1.0/i/m?url=https%3A%2F%2Fstorage.googleapis.com%2Fproduction-bluehost-v1-0-9%2F659%2F790659%2FAtmP8Pmy%2F9c8c1e647eb14e01898043c0c60bf03a&methods=resize%2C1000%2C5000',
            preview_image_url='https://images.builderservices.io/s/cdn/v1.0/i/m?url=https%3A%2F%2Fstorage.googleapis.com%2Fproduction-bluehost-v1-0-9%2F659%2F790659%2FAtmP8Pmy%2Ffd2258c5ea6c43f591e8d9930d152b94&methods=resize%2C1000%2C5000'
        ))
    else:
        print('else')
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="reply: " + event.message.text))


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)
