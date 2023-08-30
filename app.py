# https://docs.streamlit.io/library/cheatsheet
# streamlit run app.py
# import streamlit as st
# import numpy as np 
# import joblib
import base64

import streamlit as st 
from streamlit_drawable_canvas import st_canvas
from skimage import data, color, io
from skimage.transform import rescale, resize, downscale_local_mean
from skimage.color import rgb2gray, rgba2rgb

import numpy as np  
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import model_from_json


def get_image_html(page_name, file_name):
    with open(file_name, "rb") as f:
        contents = f.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    return f'<a href="{page_name}"><img src="data:image/png;base64,{data_url}" style="width:300px"></a>'

data_url = get_image_html("手寫字母", "./Hand_lettets.jpg")
data_url_2 = get_image_html("手寫數字", "./hand_numbers.jpg")
data_url_3 = get_image_html("分類", "./penguins.jpg")
data_url_4 = get_image_html("迴歸", "./taxi.png")

st.set_page_config(
    page_title="我的學習歷程",
    page_icon="✍️",
)

st.title('Machine Learning 走起來')   

col1, col2 = st.columns(2)
with col1:
    # url must be external url instead of local file
    # st.markdown(f"### [![分類]({url})](分類)")
    st.markdown('### [(CNN)手寫英文字母](手寫字母)')
    st.markdown('''
    ##### 操作方式:
        1 手寫板寫下英文字母
        2 按下辨識按鈕得辨識結果
        3 垃圾桶圖標清除手繪結果
        4 重複步驟 1
    ##### 辨識類別(Class):
        - 大寫英文字母 A - Z
        - 小寫英文字母 a - z
        ''')
    st.markdown(data_url, unsafe_allow_html=True)
    st.markdown('### [(CNN)手寫阿拉伯數字](手寫數字)')
    st.markdown('''
    ##### 操作方式:
        1 手寫板寫下阿拉伯數字
        2 按下辨識按鈕得辨識結果
        3 垃圾桶圖標清除手繪結果
        4 重複步驟 1
    ##### 辨識類別(Class):
        - 阿拉伯數字 0 - 9
        ''')
    st.markdown(data_url_2, unsafe_allow_html=True)    
with col2:
    # url must be external url instead of local file
    # st.markdown(f"### [![分類]({url})](分類)")
    st.markdown('### [(分類)企鵝品種辨識](分類)')
    st.markdown('''
    ##### 特徵(X):
        - 島嶼
        - 嘴巴長度
        - 嘴巴寬度
        - 翅膀長度
        - 體重
        - 性別
    ##### 預測類別(Class):
        - Adelie
        - Chinstrap
        - Gentoo
        ''')
    # st.image('iris.png')
    st.markdown(data_url_3, unsafe_allow_html=True)
    st.markdown('### [(迴歸)小費預測](迴歸)')
    st.markdown('''
    ##### 特徵(X):
        - 車費
        - 性別
        - 吸菸
        - 星期
        - 時間
        - 同行人數
    ##### 目標：預測小費金額
        ''')
    # st.image('taxi.png')
    st.markdown(data_url_4, unsafe_allow_html=True)

