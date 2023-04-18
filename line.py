import os
import requests
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextSendMessage, ImageMessage, ImageSendMessage, TextMessage

app = Flask(__name__)

# 設置Line Bot的Channel access token及Channel secret
line_bot_api = LineBotApi('62ZENjFkBcO5a2oDVeZikb8e1zBj7v3MgSSuR6JIYdqFEXHrp/1Riy6pq9eECx8oCfSMSHFTkLwSxKQNK9Mbiz0QXFcmiYwzC6aRFXfB8zdGEgak/3KUGRsXXG+zjvxHX7/870dygF8gKoLcPlW2zAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('f41d464e3dd13a4874b06bd2a0db1851')


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
    reply_text =  text
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )


if __name__ == '__main__':
    app.run()
