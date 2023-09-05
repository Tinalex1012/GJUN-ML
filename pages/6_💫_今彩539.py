# 若出現錯誤：TypeError: Descriptors cannot not be created directly. 可執行下列指令：
# Set PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

# streamlit user guide
# https://docs.streamlit.io/en/stable/api.html#display-interactive-widgets

import streamlit as st
import pandas as pd
import numpy as np
import datetime,requests
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from bs4 import BeautifulSoup

def download_data(year):
    url= f'http://www.olo.com.tw/histNo/mainT539.php?cp={year}'

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

def number_formula(df):
    cnt1 = np.zeros([5,40,40]).astype(np.uint8)
    for i in range(df.shape[0]-1):
        for j in range(5):
            for k in range(5):
                cnt1[0,df.iloc[i,j],(df.iloc[i+1,k])] = cnt1[0,df.iloc[i,j],(df.iloc[i+1,k])]+1
                if i < df.shape[0]-2:
                    cnt1[1,df.iloc[i,j],(df.iloc[i+2,k])] = cnt1[1,df.iloc[i,j],(df.iloc[i+2,k])]+1
                if i < df.shape[0]-3:
                    cnt1[2,df.iloc[i,j],(df.iloc[i+3,k])] = cnt1[2,df.iloc[i,j],(df.iloc[i+3,k])]+1        
                if i < df.shape[0]-4:
                    cnt1[3,df.iloc[i,j],(df.iloc[i+4,k])] = cnt1[3,df.iloc[i,j],(df.iloc[i+4,k])]+1   
                if i < df.shape[0]-5:
                    cnt1[4,df.iloc[i,j],(df.iloc[i+5,k])] = cnt1[4,df.iloc[i,j],(df.iloc[i+5,k])]+1                                      
    cnt1[cnt1<2] = 0
    df_ball=pd.DataFrame(np.array(df).ravel().astype(np.uint8),columns = ['Ball'])

    plt.figure(figsize=(16,8),constrained_layout=True)
    fig, ax = plt.subplots()
    # ax = plt.subplot(121)   
    ax = fig.gca()
    ax.set_title(f"Number statistics for the past 30{datetime.datetime.today().strftime('%Y-%m-%d')}")
    sns.countplot( x='Ball', data=df_ball)
    for p in ax.patches:
        ax.annotate(f'\n{p.get_height()}', (p.get_x(), p.get_height()), color='black', size=10)   
    st.pyplot(fig) 
    fig, ax = plt.subplots()
    item_list = []
    det_ball = pd.DataFrame()
    df_ball1 = pd.DataFrame(cnt1[0,df.iloc[-1,:].to_list(),:].T,columns=df.iloc[-1,:].to_list())
    df_ball2 = pd.DataFrame(cnt1[1,df.iloc[-2,:].to_list(),:].T,columns=df.iloc[-2,:].to_list())
    df_ball3 = pd.DataFrame(cnt1[2,df.iloc[-3,:].to_list(),:].T,columns=df.iloc[-3,:].to_list())
    df_ball4 = pd.DataFrame(cnt1[3,df.iloc[-4,:].to_list(),:].T,columns=df.iloc[-4,:].to_list())
    df_ball5 = pd.DataFrame(cnt1[4,df.iloc[-5,:].to_list(),:].T,columns=df.iloc[-5,:].to_list())
    det_ball = pd.concat([df_ball1,df_ball2,df_ball3,df_ball4,df_ball5],axis=1)
    det_ball.replace(0,None,inplace=True)
    det_ball.dropna(how='all',axis=0,inplace = True)
    # det_ball.dropna(how='all',axis=1,inplace = True)
    det_ball.replace(np.nan,0,inplace=True)
    det_ball.astype(np.uint8)
    # ax = plt.subplot(122)   
    ax.set_title(f"Predict the possible numbers{datetime.datetime.today().strftime('%Y-%m-%d')}")
    ax.set_xlabel("pass number")
    ax.set_ylabel("Predict number")
    plt.yticks(np.arange(0.5,det_ball.shape[0]+0.5),fontsize=8,rotation=90)    

    sns.heatmap(det_ball, cmap = 'PuBuGn', annot = True, linewidths = 0.5)
    ax.set_xticklabels(det_ball.columns,fontsize = 8)
    plt.gca().invert_yaxis()
    st.pyplot(fig)
    
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False

st.markdown('# 今彩539落球統計')
today = datetime.datetime.today().strftime('%Y')

df1 = download_data(str(int(today)-1912))
df2 = download_data(str(int(today)-1911))
df = pd.concat([df1,df2],ignore_index=True)
df['Date'] = pd.to_datetime(df['Date'])
df['Date'] = df['Date'].apply(lambda x: x.strftime('%Y-%m-%d'))

df.set_index('Date',inplace=True)
df.columns = ['B1','B2','B3','B4','B5']
df = df.astype(np.uint8)
i = 100
df_new = df.iloc[-i:,:]
df_new = df_new.reset_index(drop=True)

col1, col2 = st.columns(2) 
with col1:
    st.dataframe(df)
with col2:
    d = st.date_input("依日期查詢開獎號",datetime.datetime.today(),format="YYYY-MM-DD")
    if str(d) in df.index:
        st.write(f"開獎號碼:{df.loc[str(d),:].to_list()}")
        # st.write(f"{df.index} {d}")
    else:
        st.write(f"開獎號碼:暫無")


df_ball=pd.DataFrame(np.array(df_new).ravel().astype(np.uint8),columns = ['Ball'])
fig,ax = plt.subplots(figsize=(12,6), dpi=80)
ax.set_title(f"最近100期落球統計 {datetime.datetime.today().strftime('%Y-%m-%d')}")
sns.countplot( x='Ball', data=df_ball)
for p in ax.patches:
    ax.annotate(f'\n{p.get_height()}', (p.get_x(), p.get_height()), color='black', size=8)
st.pyplot(fig)

if st.button('預測下期號碼'):
    batch_items = 30
    start_number = 0
    df_p = df_new.iloc[start_number-batch_items-1:,:]
    cnt1 = number_formula(df_p)
