import pandas_datareader.data as web
import mplfinance as mpf
import pandas_datareader.data as web
import datetime
import pyimgur

IMGUR_CLIENT_ID = "80248fa08d1ca9b"


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
