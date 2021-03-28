# This is a sample Python script.
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, FlexSendMessage
)

from googletrans import Translator

import traceback
import mplfinance as mpf
import pandas_datareader.data as web
import datetime
import pyimgur

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = "bwu6x1K4VRcNmHE/yH3lPnPqNXstXYnoI1cpFlDpFGf5Ttm/nr2YjPa9zAdvJ6JbqdJAsqXJtYsb74IPSdUsVfiy9RXwmpccIN7XFs6OIGxlKhCtPPfyAPc4OWuZR/ta1RLtFi4cyNC7lhvObIOLzgdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "37baa14638d1c6f127710af279df4438"
IMGUR_CLIENT_ID = "80248fa08d1ca9b"

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


def translate_text(text, dest='en'):
    """以google翻譯將text翻譯為目標語言

    :param text: 要翻譯的字串，接受UTF-8編碼。
    :param dest: 要翻譯的目標語言，參閱googletrans.LANGCODES語言列表。
    """
    translator = Translator()
    result = translator.translate(text, dest).text
    return result


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:

        if event.source.user_id == 'U54feccad85957869d5863daaa7b7fcda':
            return 'OK'
        if event.message.text[:2] == "@E":
            content = translate_text(event.message.text[2:], "en")
            message = TextSendMessage(text=content)
            line_bot_api.reply_message(event.reply_token, message)
        if event.message.text[:2] == "@J":
            content = translate_text(event.message.text[2:], "ja")
            message = TextSendMessage(text=content)
            line_bot_api.reply_message(event.reply_token, message)
        if event.message.text[:2] == "@C":
            content = translate_text(event.message.text[2:], "zh-tw")
            message = TextSendMessage(text=content)
            line_bot_api.reply_message(event.reply_token, message)
        if event.message.text[:2].upper() == "@K":
            input_word = event.message.text.replace(" ", "")  # 合併字串取消空白
            stock_name = input_word[2:6]
            during_days = input_word[6:]
            if not during_days.strip():
                during_days = 30
            image_url = plot_stcok_k_chart(stock_name, during_days)

            flex_message = FlexSendMessage(
                alt_text=stock_name,  # alt_text
                contents={
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": image_url,
    "size": "full",
    "aspectRatio": "20:13",
    "aspectMode": "cover",
    "action": {
      "type": "uri",
      "uri": image_url
    }
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "spacing": "md",
    "contents": [
      {
        "type": "text",
        "text": stock_name,
        "wrap": True,
        "weight": "bold",
        "gravity": "center",
        "size": "xl"
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "lg",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "Period",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 1
              },
              {
                "type": "text",
                "text": str(during_days),
                "wrap": True,
                "size": "sm",
                "color": "#666666",
                "flex": 4
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "Price",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 1
              },
              {
                "type": "text",
                "text": "7 Floor, No.3",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 4
              }
            ]
          }
        ]
      }
    ]
  }
}
            )
            # message = ImageSendMessage(original_content_url=content, preview_image_url=content)
            line_bot_api.reply_message(event.reply_token, flex_message)

        else:
            line_bot_api.reply_message(event.reply_token,
                                       TextSendMessage(text=event.message.text))
    except Exception as err:
        traceback.print_exc()

def get_daily_price():
    df = web.DataReader('0050.tw', 'yahoo', '2021-03-01')
    df.tail(10)
    print(df)


def plot_stcok_k_chart(stock="0050", during_days=150, client_id=IMGUR_CLIENT_ID):
    """
  進行個股K線繪製，回傳至於雲端圖床的連結。將顯示包含5MA、20MA及量價關係。
  :stock :個股代碼(字串)，預設0050。
  :during_days :蒐集幾日前的資料，預設50日前(包含假日)，但呈現的K線會扣掉。
  """
    stock = str(stock) + ".tw"
    start_date = (datetime.datetime.now() - datetime.timedelta(int(during_days))).strftime("%Y-%m-%d")  # 計算蒐集起始日
    df = web.DataReader(stock, 'yahoo', start_date)
    mpf.plot(df.tail(int(during_days)), type='candle', mav=(5, 20), volume=True, ylabel=stock.upper() + ' Price',
             savefig='testsave.png')
    PATH = "testsave.png"
    im = pyimgur.Imgur(client_id)
    uploaded_image = im.upload_image(PATH, title=stock + " candlestick chart")
    return uploaded_image.link

if __name__ == "__main__":
    app.run(debug=True)
