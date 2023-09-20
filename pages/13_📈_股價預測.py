import streamlit as st 
import pandas as pd
import yfinance as yf
import datetime
# from matplotlib import pyplot as plt
import seaborn as sns
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.seasonal import seasonal_decompose
import statsmodels.api as sm

import matplotlib as mpl
import matplotlib.pyplot as plt 
from matplotlib.font_manager import fontManager

# 改style要在改font之前
# plt.style.use('seaborn')  

fontManager.addfont('./MODEL/design.ttf')
mpl.rc('font', family='timemachine wa')


def test_stationarity(timeseries):
    rolmean=timeseries.rolling(window=12).mean()
    rolstd=timeseries.rolling(window=12).std()
    st.markdown("**ADF檢定**")
    fig=plt.figure(figsize=(12,4))
    orig=plt.plot(timeseries,color='blue',label='一次差分')
    mean=plt.plot(rolmean,color='red',label='移動平均')
    std=plt.plot(rolstd,color='black',label='標準差')
    plt.legend(loc='best')
    plt.title('一次差分 移動平均 & 標準差')
    st.pyplot(fig)
    
    # Perform Dickey-Fuller test:
    # Dickey-Fuller test is used to determine whether a unit root (a feature that can cause 
    # issues in statistical inference) is present in an autoregressive model.
    st.text('Results of Dickey-Fuller Test:')
    dftest=adfuller(timeseries,autolag='AIC')
    dfoutput=pd.Series(dftest[0:4],index=['ADF統計量','p-value','滯後期數(#Lags)','資料筆數'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value(%s)'%key]=value
    st.text(dfoutput)

    fig=plt.figure(figsize=(12,6),constrained_layout=True)
    ax1=fig.add_subplot(211)
    fig=sm.graphics.tsa.plot_acf(timeseries,lags=20,ax=ax1)
    ax2=fig.add_subplot(212)
    fig=sm.graphics.tsa.plot_pacf(timeseries,lags=20,ax=ax2)
    st.pyplot(fig)

    fig, axarr = plt.subplots(4, sharex=True)
    fig.set_size_inches(12, 6)

st.title("台股股價預測")
# plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
# plt.rcParams['axes.unicode_minus'] = False

stock_list = pd.read_excel('./MODEL/stock_list.xlsx')  
today = datetime.date.today()
dateStart = (today - datetime.timedelta(days=365*4)).strftime('%Y-%m-%d')    # 載入三年資料
dateEnd = today.strftime('%Y-%m-%d')  
target_stock=""
draw_chk = 0

col1, col2 = st.columns([1, 5])
with col1:
    target_stock = f"{st.text_input('台股代號')}"
    try:
        download_chk = 0
        df = yf.download(f'{target_stock}.TW', start=dateStart, end=dateEnd)
        df_close = df[['Adj Close']].copy()
        df_close.columns = ['Close']
        stock_name = stock_list[stock_list['代號']==int(target_stock)]['股票名稱'].values[0]        
        download_chk = 1
    except:
        st.text(f'查無此股票')
        draw_chk = 0
    if download_chk == 1:
        if st.button('股價預測'):
            draw_chk=1


with col2:
    try:
        if draw_chk == 1 & download_chk==1:
            fig = plt.figure(figsize=(8, 5))
            plt.title(f'{target_stock} {stock_name} 收盤線圖 ')
            sns.lineplot(x=df_close.index, y='Close', data=df_close )
            st.pyplot(fig)
    except:
         st.text(f'查無此股票')

try:
    if draw_chk == 1 & download_chk==1 :

        df_diff = pd.DataFrame()
        df_diff['Adj Close'] = df['Adj Close'].copy()
        df_diff['diff'] = df['Adj Close'] - df['Adj Close'].shift(1)
        test_stationarity(df_diff['diff'].dropna(inplace=False))

        date1 = pd.date_range(start=df.index[0], end=df.index[-1])
        decomp = pd.DataFrame(index=date1)
        decomp = decomp.join(df)
        decomp = decomp.fillna(method='ffill')

        s_dc = seasonal_decompose(decomp['Adj Close'], model='additive')
        decomp['SDC_Seasonal'] = s_dc.seasonal
        decomp['SDC_Trend'] = s_dc.trend
        decomp['SDC_Error'] = s_dc.resid
        decomp['SDC_TS'] = s_dc.trend + s_dc.seasonal
        st.markdown("**效應分解**")
        fig=plt.figure(figsize=(12,6),constrained_layout=True)
        ax1 = fig.add_subplot(411)
        ax1 = decomp['Adj Close'].plot(ax=ax1, color='b', linestyle='-',title="實際值")
        ax2 = fig.add_subplot(412)
        ax2 = pd.Series(data=decomp['SDC_Trend'], index=decomp.index).plot(color='r', linestyle='-', ax=ax2, title="趨勢")
        ax3 = fig.add_subplot(413)
        ax3 = pd.Series(data=decomp['SDC_Seasonal'], index=decomp.index).plot(color='g', linestyle='-', ax=ax3, title="週期效應")
        ax4 = fig.add_subplot(414)
        ax4 = pd.Series(data=decomp['SDC_Error'], index=decomp.index).plot(color='k', linestyle='-', ax=ax4, title="殘差")
        st.pyplot(fig)

        st.markdown("**時間序列**") 
        MSE = (decomp['SDC_Error']**2).sum() / decomp['SDC_Error'].shape[0]
        for _ in range(3,len(decomp)):
            if (decomp.iloc[_:_+1,6][0] == decomp.iloc[0:1,6][0])&(decomp.iloc[_+1:_+2,6][0] == decomp.iloc[1:2,6][0]) & (decomp.iloc[_+2:_+3,6][0] == decomp.iloc[2:3,6][0]):
                period_num = _
                break
        df_SARIMAX = df_diff.copy()
        train=df_SARIMAX[:int(df_SARIMAX.shape[0]*0.9)]
        test=df_SARIMAX[int(df_SARIMAX.shape[0]*0.9):]
        mod=sm.tsa.statespace.SARIMAX(train['diff'],trend='n',order=(0,1,1),seasonal_order=(1,1,0,period_num))
        results=mod.fit()
        st.text(results.summary())
        st.markdown(f"**MSE = {MSE}**") 
        st.markdown("**股價預測**") 
        tmp = results.predict(start = int(df_SARIMAX.shape[0]*0.9)+1, end= df_SARIMAX.shape[0], dynamic= True).to_list()
        test['diff_pred'] = tmp
        test[['diff', 'diff_pred']].plot(figsize=(12, 6))
        x, x_diff = test['Adj Close'].iloc[:], test['diff_pred'].iloc[:]
        C=[]
        for i in range(len(x)-1):
            c=x[i]+x_diff[i+1]
            C.append(c)
        C=[0]*1+C
        test['pred']=C

        day_list = [(today + datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1, period_num+1)]
        pred_df = pd.DataFrame(columns=['Adj Close', 'diff', 'diff_pred','pred'], index = day_list)
        last_price = test[-1:]['pred'].values[0]
        tmp1 = results.predict(start = df_SARIMAX.shape[0]+1, end= df_SARIMAX.shape[0]+period_num, dynamic= True).to_list()
        pred_df['diff_pred']=tmp1[-period_num:]
        pred_df.iloc[0:1,3] = last_price + pred_df[0:1]['diff_pred'].values[0]
        for i in range(1,len(pred_df)):
            pred_df.iloc[i:i+1,3] = pred_df.iloc[i-1]['pred'] + pred_df.iloc[i]['diff_pred']
        test = pd.concat([test,pred_df],axis=0)
        test.index = pd.to_datetime(test.index)
        test.columns = ['實際收盤','diff','diff_pred','預測值']
        fig_pred = plt.figure(figsize=(12, 6))
        plt.title(f'{target_stock} {stock_name} 收盤價預測圖')
        plt.plot(test[period_num:]['預測值'],color='red',label='預測值')
        plt.plot(test[period_num:]['實際收盤'],color='blue',label='實際收盤')
        plt.legend(loc='best')
        st.pyplot(fig_pred)

except:
    st.text(f'查無此股票')




