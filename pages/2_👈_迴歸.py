# https://docs.streamlit.io/library/cheatsheet
# streamlit run app.py
import streamlit as st
import numpy as np
import joblib

# load model
clf2 = joblib.load('tips.joblib')
scaler = joblib.load('tips_scaler.joblib')

sex_dict = {'Female':0, 'Male':1}
smoker_dict = {'No':0, 'Yes':1}
day_dict = {'Sun':4, 'Sat':3, 'Fri':2, 'Thur':1}
time_dict = {'Dinner':0, 'Lunch':1}

# 畫面設計
st.markdown('# 計程車小費預測系統')
col1, col2 = st.columns(2)

with col1:
    total_bill = st.slider('車費', 0, 50, 10)
    sex = st.radio('性別', sex_dict.keys())
    smoker = st.radio('吸菸', smoker_dict.keys())
with col2:
    day1 = st.selectbox('星期', day_dict.keys())
    time1 = st.selectbox('時間', time_dict.keys())
    size1 = st.slider('同行人數', 1, 5, 2)
    
if st.button('預測'):
    # predict
    X=np.array([[total_bill, sex_dict[sex], smoker_dict[smoker], day_dict[day1]
                , time_dict[time1], size1]])
    X=scaler.transform(X)
    st.markdown(f'預測結果： **{clf2.predict(X)[0]:.2f}**')    