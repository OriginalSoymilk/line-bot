import os
import requests
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextSendMessage, ImageMessage, ImageSendMessage, TextMessage

app = Flask(__name__)

# 設置Line Bot的Channel access token及Channel secret
line_bot_api = LineBotApi('K7jkNovEJpCqafdqEuZh1TFGcr5JegkjJHC6l6v2+ZfLlNoByJUGgGnuY6yJ3dELGESLXwru742Ku2ijGgGtUHJ2150By86Wj6kzZKySFnmkyU4jHhK//pyfRoi4bU/VvGS/wKeOzBYP8NyV3q1CqQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('2a9a171886e678889fc9972e25c3580c')


# Line Bot接收Webhook的路由
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
def handle_message(event):
    text = event.message.text
    reply_text = 'Hello, you said: ' + text
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )


if __name__ == '__main__':
    app.run()
