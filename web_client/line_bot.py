from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)

from googletrans import Translator

from build.lib.web_client import get_data

app = Flask(__name__)

from config import *


LINE_CHANNEL_ACCESS_TOKEN = "bwu6x1K4VRcNmHE/yH3lPnPqNXstXYnoI1cpFlDpFGf5Ttm/nr2YjPa9zAdvJ6JbqdJAsqXJtYsb74IPSdUsVfiy9RXwmpccIN7XFs6OIGxlKhCtPPfyAPc4OWuZR/ta1RLtFi4cyNC7lhvObIOLzgdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "37baa14638d1c6f127710af279df4438"

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

def translate_text(text,dest='en'):
    """以google翻譯將text翻譯為目標語言

    :param text: 要翻譯的字串，接受UTF-8編碼。
    :param dest: 要翻譯的目標語言，參閱googletrans.LANGCODES語言列表。
    """
    translator = Translator()
    result = translator.translate(text, dest).text
    return result


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.source.user_id =='Udeadbeefdeadbeefdeadbeefdeadbeef':
        return 'OK'
    if event.message.text[:3] == "@翻英":
        content = translate_text(event.message.text[3:], "en")
        message = TextSendMessage(text=content)
        line_bot_api.reply_message(event.reply_token, message)
    if event.message.text[:3] == "@翻日":
        content = translate_text(event.message.text[3:] , "ja")
        message = TextSendMessage(text=content)
        line_bot_api.reply_message(event.reply_token, message)
    if event.message.text[:3] == "@翻中":
        content = translate_text(event.message.text[3:] , "zh-tw")
        message = TextSendMessage(text=content)
        line_bot_api.reply_message(event.reply_token, message)
    if event.message.text[:2].upper() == "@K":
        input_word = event.message.text.replace(" ","") #合併字串取消空白
        stock_name = input_word[2:6] #2330
        start_date = input_word[6:] #2020-01-01
        content = get_data.plot_stcok_k_chart(stock_name,start_date)
        message = ImageSendMessage(original_content_url=content,preview_image_url=content)
        line_bot_api.reply_message(event.reply_token, message)

    else: line_bot_api.reply_message(event.reply_token,
                                     TextSendMessage(text=event.message.text))