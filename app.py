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
    return f'<a href="{page_name}"><img src="data:image/png;base64,{data_url}" style="width:200px"></a>'


data_url_1 = get_image_html("年所得預測", "./image/HW01.jpg")
data_url_2 = get_image_html("分類", "./image/penguins.jpg")
data_url_3 = get_image_html("迴歸", "./image/taxi.png")
data_url_4 = get_image_html("聯立方程式", "./image/Function.jpg")
data_url_5 = get_image_html("梯度下降法", "./image/GD.png")
data_url_6 = get_image_html("今彩539", "./image/539.jpg")
data_url_7_1 = get_image_html("手寫字母", "./image/Hand_lettets.jpg")
data_url_7_2 = get_image_html("手寫數字", "./image/hand_numbers.jpg")
data_url_8_1 = get_image_html("圖像辨識", "./image/8_1.jpg")
data_url_8_2 = get_image_html("圖片辨識", "./image/8_2.png")

st.set_page_config(
    page_title="我的學習歷程",
    page_icon="✍️",
)

st.title('Machine Learning 走起來')   
link='[Github ](https://github.com/Tinalex1012/GJUN-ML)'
st.markdown(link,unsafe_allow_html=True)

homework_list = ["作業二","作業三","作業四","作業六","作業七","作業八","作業九","作業十"]
tab_list= st.tabs(homework_list)

####################### 作業二 #######################
with tab_list[0]:
    st.header("作業二")
    col = st.columns(3)
    with col[0]:
        st.markdown('#### [(分類)年所得預測](年所得預測)')
        st.markdown('''
        ##### 操作方式:
            1 調整屬性數值
            2 按下預測按鈕得預測結果
        ##### 輸出結果:
            - 預測年收入>50K 或 <50K
            ''')
        st.markdown(data_url_1, unsafe_allow_html=True)
    with col[1]:
        st.markdown('#### [(分類)企鵝品種辨識](分類)')
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
        st.markdown(data_url_2, unsafe_allow_html=True)
    with col[2]:
        st.markdown('#### [(迴歸)小費預測](迴歸)')
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
        st.markdown(data_url_3, unsafe_allow_html=True)

####################### 作業三 #######################
with tab_list[1]:
    st.header("作業三")
    st.markdown('### [(Sympy)解聯立方程式](聯立方程式)')
    st.markdown('''
    ##### 操作方式:
        1 寫下聯立方程式
        2 按下結果按鈕
    ##### 輸出(Output):
        - 求解聯立方程式
        ''')
    st.markdown(data_url_4, unsafe_allow_html=True)    

####################### 作業四 #######################
with tab_list[2]:
    st.header("作業四")
    st.markdown('### [(Sympy)梯度下降法](梯度下降法)')
    st.markdown('''
    ##### 操作方式:
        1 調整學習率等參數
    ##### 輸出(Output):
        - 演示梯度下降法過程
        ''')
    st.markdown(data_url_5, unsafe_allow_html=True)    

####################### 作業六 #######################
with tab_list[3]:
    st.header("作業六")
    st.markdown('### [(機率)今彩539](今彩539)')
    st.markdown('''
    ##### 操作方式:
        1 設定查詢日期
        2 依拖牌版路預測下期號碼
    ##### 輸出(Output):
        - 統計查詢日期近30期落球數
        - 拖牌版路統計數
        ''')
    st.markdown(data_url_6, unsafe_allow_html=True)  

####################### 作業七 #######################
with tab_list[4]:
    st.header("作業七")
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
        st.markdown(data_url_7_1, unsafe_allow_html=True)
    with col2:
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
        st.markdown(data_url_7_2, unsafe_allow_html=True)    

####################### 作業八 #######################
with tab_list[5]:
    st.header("作業八")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('### [(CNN)Intel Image](圖像辨識)')
        st.markdown('''
        ##### 操作方式:
            1 上傳圖片辨識圖像
            2 按下圖像辨識按鈕得辨識結果
        ##### 辨識類別(Class):
            - 建築物 
            - 森林
            - 冰川
            - 山景
            - 海景
            - 街景
            ''')
        st.markdown(data_url_8_1, unsafe_allow_html=True)
    with col2:
        st.markdown('### [(Fmnist)圖片辨識](圖片辨識)')
        st.markdown('''
        ##### 操作方式:
            1 上傳圖片辨識圖像
            2 按下圖像辨識按鈕得辨識結果
        ##### 辨識類別(Class):
            - 0 - 短袖汗衫
            - 1 - 褲子
            - 2 - 套衫
            - 3 - 裙子
            - 4 - 外套
            - 5 - 涼鞋
            - 6 - 襯衫
            - 7 - 運動鞋
            - 8 - 包包
            - 9 - 長靴                 
            ''')
        st.markdown(data_url_8_2, unsafe_allow_html=True) 



