# streamlit run HW03_web_Solution

# 若出現錯誤：TypeError: Descriptors cannot not be created directly. 可執行下列指令：
# Set PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

# streamlit user guide
# https://docs.streamlit.io/en/stable/api.html#display-interactive-widgets

import streamlit as st
import pandas as pd
# import numpy as np
import datetime,requests
import seaborn as sns
from bs4 import BeautifulSoup
from statsmodels.tsa.seasonal import seasonal_decompose
import statsmodels.api as sm
import matplotlib as mpl
import matplotlib.pyplot as plt 
from matplotlib.font_manager import fontManager
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller

def download_data(year):
    url= f'http://www.olo.com.tw/histNo/mainT539.php?cp={year}&St1=1'

    # 送出要求，並取得回應資料
    response = requests.post(url)
    # response.status_code
    soup = BeautifulSoup(response.text)
    data = []
    table = soup.find('table')
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele]) # Get rid of empty values
    data = data[2:-1]
    columns = ['no','n1', 'n2', 'n3', 'n4', 'n5', 'Date']
    df = pd.DataFrame(data, columns=columns)
    df = df.dropna()
    df.drop('no',axis=1,inplace=  True)
    return df


fontManager.addfont('./MODEL/design.ttf')
mpl.rc('font', family='timemachine wa')
st.header("今彩539 時間序列預測彩號")
st.markdown('今彩539落球統計')
pred_out_chk = 0
today = datetime.datetime.today().strftime('%Y')

df1 = download_data(str(int(today)-1914))
df2 = download_data(str(int(today)-1913))
df3 = download_data(str(int(today)-1912))
df4 = download_data(str(int(today)-1911))

data = pd.concat([df1,df2,df3,df4],ignore_index=True)
data1 = data.copy()
data['Date'] = pd.to_datetime(data['Date'])
data1['Date'] = pd.to_datetime(data1['Date']).dt.strftime('%Y-%m-%d')
data.set_index('Date',inplace=True)
data1.set_index('Date',inplace=True)
data.columns = ['B1','B2','B3','B4','B5']
data1.columns = ['B1','B2','B3','B4','B5']
data[['B1','B2','B3','B4','B5']] = data[['B1','B2','B3','B4','B5']].astype('uint8')

col1, col2 = st.columns(2) 
with col1:
    st.dataframe(data1[-30:])
with col2:
    d = st.date_input("依日期查詢開獎號",datetime.datetime.today(),format="YYYY-MM-DD")
    if str(d) in data.index:
        st.write(f"開獎號碼:{data.loc[str(d),:].to_list()}")
        # st.write(f"{df.index} {d}")
    else:
        st.write(f"開獎號碼:暫無")
    
    if st.button('預測本期號碼'):

        df_diff = pd.DataFrame()
        df_diff['dB1'] = data['B1'] - data['B1'].shift(1)
        df_diff['dB2'] = data['B2'] - data['B2'].shift(1)
        df_diff['dB3'] = data['B3'] - data['B3'].shift(1)
        df_diff['dB4'] = data['B4'] - data['B4'].shift(1)
        df_diff['dB5'] = data['B5'] - data['B5'].shift(1)
        # df_diff.dropna(inplace=True)        
        df_diff['d2B1'] = df_diff['dB1'] - df_diff['dB1'].shift(1)
        df_diff['d2B2'] = df_diff['dB2'] - df_diff['dB2'].shift(1)
        df_diff['d2B3'] = df_diff['dB3'] - df_diff['dB3'].shift(1)
        df_diff['d2B4'] = df_diff['dB4'] - df_diff['dB4'].shift(1)
        df_diff['d2B5'] = df_diff['dB5'] - df_diff['dB5'].shift(1)        
        df_diff.dropna(inplace=True)

        date1 = pd.date_range(start=data.index[0], end=data.index[-1])
        decomp = pd.DataFrame(index=date1)
        decomp = decomp.join(data)
        decomp = decomp.fillna(method='ffill')

        sde = pd.DataFrame()
        s_dc = seasonal_decompose(decomp['B1'], model='additive')
        decomp['SDS1'] = s_dc.seasonal
        sde['SDE1'] = s_dc.resid
        MSE1 = (sde['SDE1']**2).sum() / sde['SDE1'].shape[0]
        for _ in range(3,len(decomp)):
            if (decomp.iloc[_:_+1,5][0] == decomp.iloc[0:1,5][0])&(decomp.iloc[_+1:_+2,5][0] == decomp.iloc[1:2,5][0]) & (decomp.iloc[_+2:_+3,5][0] == decomp.iloc[2:3,5][0]):
                period_num1 = _
                break
        s_dc = seasonal_decompose(decomp['B2'], model='additive')
        decomp['SDS2'] = s_dc.seasonal
        sde['SDE2'] = s_dc.resid
        MSE2 = (sde['SDE2']**2).sum() / sde['SDE2'].shape[0]
        for _ in range(3,len(decomp)):
            if (decomp.iloc[_:_+1,6][0] == decomp.iloc[0:1,6][0])&(decomp.iloc[_+1:_+2,6][0] == decomp.iloc[1:2,6][0]) & (decomp.iloc[_+2:_+3,6][0] == decomp.iloc[2:3,6][0]):
                period_num2 = _
                break
        s_dc = seasonal_decompose(decomp['B3'], model='additive')
        decomp['SDS3'] = s_dc.seasonal
        sde['SDE3'] = s_dc.resid
        MSE3 = (sde['SDE3']**2).sum() / sde['SDE3'].shape[0]
        for _ in range(3,len(decomp)):
            if (decomp.iloc[_:_+1,7][0] == decomp.iloc[0:1,7][0])&(decomp.iloc[_+1:_+2,7][0] == decomp.iloc[1:2,7][0]) & (decomp.iloc[_+2:_+3,7][0] == decomp.iloc[2:3,7][0]):
                period_num3 = _
                break
        s_dc = seasonal_decompose(decomp['B4'], model='additive')
        decomp['SDS4'] = s_dc.seasonal
        sde['SDE4'] = s_dc.resid
        MSE4 = (sde['SDE4']**2).sum() / sde['SDE4'].shape[0]
        for _ in range(3,len(decomp)):
            if (decomp.iloc[_:_+1,8][0] == decomp.iloc[0:1,8][0])&(decomp.iloc[_+1:_+2,8][0] == decomp.iloc[1:2,8][0]) & (decomp.iloc[_+2:_+3,8][0] == decomp.iloc[2:3,8][0]):
                period_num4 = _
                break
        s_dc = seasonal_decompose(decomp['B5'], model='additive')
        decomp['SDS5'] = s_dc.seasonal
        sde['SDE5'] = s_dc.resid
        MSE5 = (sde['SDE5']**2).sum() / sde['SDE5'].shape[0]
        for _ in range(3,len(decomp)):
            if (decomp.iloc[_:_+1,9][0] == decomp.iloc[0:1,9][0])&(decomp.iloc[_+1:_+2,9][0] == decomp.iloc[1:2,9][0]) & (decomp.iloc[_+2:_+3,9][0] == decomp.iloc[2:3,9][0]):
                period_num5 = _
                break

        df_SARIMAX = data.copy()
        train=df_SARIMAX[:int(df_SARIMAX.shape[0])]
        # test=df_SARIMAX[int(df_SARIMAX.shape[0]*0.9):]
        mod1=sm.tsa.statespace.SARIMAX(train['B1'],trend='n',order=(0,1,1),seasonal_order=(1,1,0,period_num3))
        results1=mod1.fit()
        mod2=sm.tsa.statespace.SARIMAX(train['B2'],trend='n',order=(0,1,1),seasonal_order=(1,1,0,period_num3))
        results2=mod2.fit()
        mod3=sm.tsa.statespace.SARIMAX(train['B3'],trend='n',order=(0,1,1),seasonal_order=(1,1,0,period_num3))
        results3=mod3.fit()
        mod4=sm.tsa.statespace.SARIMAX(train['B4'],trend='n',order=(0,1,1),seasonal_order=(1,1,0,period_num3))
        results4=mod4.fit()
        mod5=sm.tsa.statespace.SARIMAX(train['B5'],trend='n',order=(0,1,1),seasonal_order=(1,1,0,period_num3))
        results5=mod5.fit()

        tmp = [0 for _ in range(5)]
        tmp[0] = int(results1.predict(start = df_SARIMAX.shape[0], end= df_SARIMAX.shape[0], dynamic= True))
        tmp[1] = int(results2.predict(start = df_SARIMAX.shape[0], end= df_SARIMAX.shape[0], dynamic= True))
        tmp[2] = int(results3.predict(start = df_SARIMAX.shape[0], end= df_SARIMAX.shape[0], dynamic= True))
        tmp[3] = int(results4.predict(start = df_SARIMAX.shape[0], end= df_SARIMAX.shape[0], dynamic= True))
        tmp[4] = int(results5.predict(start = df_SARIMAX.shape[0], end= df_SARIMAX.shape[0], dynamic= True))
        st.write(f'預測下期號碼：{tmp}')
        pred_out_chk = 1

ball_list = ["彩號一","彩號二","彩號三","彩號四","彩號五"]
if pred_out_chk == 1:
    tab_list= st.tabs(ball_list)
    with tab_list[0]:
        st.markdown('彩號一分析')
        st.markdown(f'***MSE = {MSE1:.2f}***')
        st.markdown(f'一次差分')
        result = adfuller(df_diff['dB1'])
        st.text(f' ADF: {result[0]:2.2e}\n p-value: {result[1]:2.2e}\n 滯後期數(Lags): {result[2]}\n 資料筆數 {result[3]}')
        fig = plot_acf(df_diff['dB1'], lags=20)
        fig.set_size_inches(10, 3)
        st.pyplot(fig)
        fig = plot_pacf(df_diff['dB1'], lags=20)
        fig.set_size_inches(10, 3)
        st.pyplot(fig)
        st.markdown(f'二次差分')
        fig = plot_acf(df_diff['d2B1'], lags=20)
        fig.set_size_inches(10, 3)
        st.pyplot(fig)
        fig = plot_pacf(df_diff['d2B1'], lags=20)
        fig.set_size_inches(10, 3)
        st.pyplot(fig)        
        st.text(results1.summary())
    with tab_list[1]:
        st.markdown('彩號二分析')
        st.markdown(f'***MSE = {MSE2:.2f}***')
        st.markdown(f'一次差分')
        result = adfuller(df_diff['dB2'])
        st.text(f' ADF: {result[0]:2.2e}\n p-value: {result[1]:2.2e}\n 滯後期數(Lags): {result[2]}\n 資料筆數 {result[3]}')      
        fig = plot_acf(df_diff['dB2'], lags=20)
        fig.set_size_inches(10, 3)
        st.pyplot(fig)
        fig = plot_pacf(df_diff['dB2'], lags=20)
        fig.set_size_inches(10, 3)
        st.pyplot(fig)        
        st.markdown(f'二次差分')
        fig = plot_acf(df_diff['d2B2'], lags=20)
        fig.set_size_inches(10, 3)
        st.pyplot(fig)
        fig = plot_pacf(df_diff['d2B2'], lags=20)
        fig.set_size_inches(10, 3)
        st.pyplot(fig)                
        st.text(results2.summary())
    with tab_list[2]:
        st.markdown('彩號三分析')
        st.markdown(f'***MSE = {MSE3:.2f}***')
        st.markdown(f'一次差分')
        result = adfuller(df_diff['dB3'])
        st.text(f' ADF: {result[0]:2.2e}\n p-value: {result[1]:2.2e}\n 滯後期數(Lags): {result[2]}\n 資料筆數 {result[3]}')      
        fig = plot_acf(df_diff['dB3'], lags=20)
        fig.set_size_inches(10, 3)
        st.pyplot(fig)
        fig = plot_pacf(df_diff['dB3'], lags=20)
        fig.set_size_inches(10, 3)
        st.pyplot(fig)        
        st.markdown(f'二次差分')
        fig = plot_acf(df_diff['d2B3'], lags=20)
        fig.set_size_inches(10, 3)
        st.pyplot(fig)
        fig = plot_pacf(df_diff['d2B3'], lags=20)
        fig.set_size_inches(10, 3)
        st.pyplot(fig)                
        st.text(results3.summary())
    with tab_list[3]:
        st.markdown('彩號四分析')
        st.markdown(f'***MSE = {MSE4:.2f}***')
        st.markdown(f'一次差分')
        result = adfuller(df_diff['dB4'])
        st.text(f' ADF: {result[0]:2.2e}\n p-value: {result[1]:2.2e}\n 滯後期數(Lags): {result[2]}\n 資料筆數 {result[3]}')       
        fig = plot_acf(df_diff['dB4'], lags=20)
        fig.set_size_inches(10, 3)
        st.pyplot(fig)
        fig = plot_pacf(df_diff['dB4'], lags=20)
        fig.set_size_inches(10, 3)
        st.pyplot(fig)        
        st.markdown(f'二次差分')
        fig = plot_acf(df_diff['d2B4'], lags=20)
        fig.set_size_inches(10, 3)
        st.pyplot(fig)
        fig = plot_pacf(df_diff['d2B4'], lags=20)
        fig.set_size_inches(10, 3)
        st.pyplot(fig)                
        st.text(results4.summary())
    with tab_list[4]:
        st.markdown('彩號五分析')
        st.markdown(f'***MSE = {MSE5:.2f}***')
        st.markdown(f'一次差分')
        result = adfuller(df_diff['dB5'])
        st.text(f' ADF: {result[0]:2.2e}\n p-value: {result[1]:2.2e}\n 滯後期數(Lags): {result[2]}\n 資料筆數 {result[3]}')       
        fig = plot_acf(df_diff['dB5'], lags=20)
        fig.set_size_inches(10, 3)
        st.pyplot(fig)
        fig = plot_pacf(df_diff['dB5'], lags=20)
        fig.set_size_inches(10, 3)
        st.pyplot(fig)        
        st.markdown(f'二次差分')
        fig = plot_acf(df_diff['d2B5'], lags=20)
        fig.set_size_inches(10, 3)
        st.pyplot(fig)
        fig = plot_pacf(df_diff['d2B5'], lags=20)
        fig.set_size_inches(10, 3)
        st.pyplot(fig)                
        st.text(results5.summary())
