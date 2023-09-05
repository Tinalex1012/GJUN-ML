import streamlit as st 
import pandas as pd
import yfinance as yf
import datetime
import mplfinance as mpf
import requests,json


def KValue(rsv):
    global K
    K = (2/3) * K + (1/3) * rsv
    return K

def DValue(k):
    global D
    D = (2/3) * D + (1/3) * k
    return D
def twse_data(r_data:str):
    data = requests.get(f'https://www.twse.com.tw/rwd/zh/fund/T86?date={r_data}&selectType=ALLBUT0999&response=json&_=1687757740217')
    data_json = json.loads(data.text)
    df = pd.DataFrame(data_json['data'],columns=data_json['fields'])
    df = df.replace(',','', regex=True)
    return df
k_map = {'日K':0, '周K':1}

st.title("台股一年K線繪製")
col1, col2 = st.columns([1, 5])
with col1:
    stock = f"{st.text_input('台股代號')}.TW"
    k_show = st.radio('K線', k_map.keys())
    bb_show = st.checkbox('布林通道')
    kd_show = st.checkbox('KD')
    macd_show = st.checkbox('MACD')
    dateEnd = st.date_input("起始日期",datetime.datetime.today(),format="YYYY-MM-DD")
with col2:
    if st.button('繪製K線'):
        
        dateStart = (dateEnd - datetime.timedelta(days=365)).strftime('%Y-%m-%d')
        dateEnd = dateEnd.strftime('%Y-%m-%d')  
        try:
            df = yf.download(stock, start=dateStart, end=dateEnd)
            df.columns = ['open','high','low','close','adj Close','volume']

            df['9MAX'] = df['high'].rolling('9D').max()
            df['9MIN'] = df['low'].rolling('9D').min()
            # 計算每日 RSV 值
            df['RSV'] = 100 * (df['close'] - df['9MIN']) / (df['9MAX'] - df['9MIN'])

            # 計算KD
            K = 0
            df['K'] = df['RSV'].apply(KValue)

            # 計算 D 值
            D = 0
            df['D'] = df['K'].apply(DValue)

            exp1 = df['close'].ewm(span=12, adjust=False).mean()
            exp2 = df['close'].ewm(span=26, adjust=False).mean()
            # 計算MACD 和 Signal line
            df['MACD'] = exp1 - exp2
            df['Signal line'] = df['MACD'].ewm(span=9, adjust=False).mean()

            # 計算 布林指標
            df['BB'] = df['close'].rolling(20).mean()
            df['UB'] = df['BB'] + 2*df['close'].rolling(20).std()
            df['LB'] = df['BB'] - 2*df['close'].rolling(20).std()

            mc = mpf.make_marketcolors(up='red',down='green',inherit=True)
            s  = mpf.make_mpf_style(base_mpf_style='starsandstripes',marketcolors=mc)
            if k_show == '日K':
                panel_select = 2
                add_plot = []
                if bb_show:
                    add_plot.append(mpf.make_addplot(df[['UB','LB']],linestyle='dashdot'))
                    add_plot.append(mpf.make_addplot(df['BB'],linestyle='dotted',color='y'))
                if kd_show:
                    add_plot.append(mpf.make_addplot(df["K"],panel= panel_select,color="b"))
                    add_plot.append(mpf.make_addplot(df["D"],panel= panel_select,color="r"))
                    panel_select += 1
                if macd_show:
                    add_plot.append(mpf.make_addplot(df["MACD"],panel= panel_select,color="b"))
                    add_plot.append(mpf.make_addplot(df["Signal line"],panel= panel_select,color="r"))
                    add_plot.append(mpf.make_addplot(df["Signal line"]-df["MACD"],panel= panel_select,type='bar',width=0.5))
                kwargs = dict(type='candle', volume = True,figsize=(20, 10),title = stock, style=s,addplot=add_plot)
                fig = mpf.plot(df, **kwargs)
                st.set_option('deprecation.showPyplotGlobalUse', False)
                st.pyplot(fig)
            else:
                df1 = df.resample('w').last()
                fig = mpf.plot(df1, type='candle', style=s, volume=True, title=stock, tight_layout=True)
                st.set_option('deprecation.showPyplotGlobalUse', False)
                st.pyplot(fig)
        except:
            st.text(f'查無此股票')


if st.button('法人買賣超'):
    today = datetime.date.today()
    control = 0
    for i in range(1,11):
        if control <=2 :
            try:
                date_target = today - datetime.timedelta(days=(i))
                convert_date = date_target.strftime('%Y%m%d')
                data = twse_data(convert_date)
                # 獲取買超前50名
                d_b = data.head(50)
                # 獲取賣超前50名
                d_s = data.tail(50)
                if control == 0:
                    resultB = set(d_b[u'證券代號'].to_list())
                    resultS = set(d_s[u'證券代號'].to_list())
                else:
                    resultB = resultB.intersection(set(d_b[u'證券代號'].to_list()))
                    resultS = resultS.intersection(set(d_s[u'證券代號'].to_list()))
                control += 1
            except: 
                continue
        else:
            break
    resultB = list(resultB)
    resultS = list(resultS)
    dfB = pd.DataFrame()
    dfB['日期'] = len(resultB)*[today]
    dfB['代號'] = resultB
    dfB['鉅亨網連結'] = dfB['代號'].apply(lambda x:f"https://www.cnyes.com/twstock/{x}")
    dfS = pd.DataFrame()
    dfS['日期'] = len(resultS)*[today]
    dfS['代號'] = resultS
    dfS['鉅亨網連結'] = dfS['代號'].apply(lambda x:f"https://www.cnyes.com/twstock/{x}")
    st.write(f'連續三日法人買超')
    st.dataframe(dfB)
    st.write(f'連續三日法人賣超')
    st.dataframe(dfS)
    # body = f'''<html>
    #             <body>
    #             <h4>連續三日法人買超</h4>
    #             {dfB.to_html(index=False)}
    #             <h4>連續三日法人賣超</h4>
    #             {dfS.to_html(index=False)}
    #             </body>
    #             </html>'''
    # st.write(body,unsafe_allow_html=True)