import streamlit as st
import joblib,csv
import base64

def get_image_html(file_name):
    with open(file_name, "rb") as f:
        contents = f.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    return f'<a href=""><img src="data:image/png;base64,{data_url}" style="width:400px"></a>'


# 載入模型與標準化轉換模型
s_model = joblib.load('./MODEL/S_Titanic.joblib')
scaler = joblib.load('./MODEL/S_Titanic_scaler.joblib')

list1 = [0 for _ in range(13)]
st.title('太空鐵達尼事件簿')
st.header('事件描述')
description_Text = '''
         歡迎來到 2912 年，需要您的數據科學技能來解開宇宙之謎。 我們收到了來自四光年外的信號，\n
         情況看起來不太好。\n
         泰坦尼克號宇宙飛船是一個月前下水的一艘星際客輪。 船上載有近 13,000 名乘客，這艘船開始\n
         了它的處女航，將太陽系的移民運送到繞附近恆星運行的三顆新的宜居系外行星。在繞行半人馬座\n
         阿爾法星前往其第一個目的地（巨蟹座55e）途中，粗心的泰坦尼克號宇宙飛船與隱藏在塵埃雲中\n
         的時空異常相撞。\n
         可悲的是，它遭遇了與 1000 年前同名的相似命運。 雖然飛船完好無損，但幾乎一半的乘客都被\n
         傳送到了異次元！\n
         輸入參數尋找倖存者！
'''
st.text(description_Text)
st.text('預測準確率 : 80%')

# HomePlanet      0
# Destination     1
# Age             2
# RoomService	    3
# FoodCourt       4
# ShoppingMall    5
# Spa	            6
# VRDeck          7
# family_size	    8
# Deck            9
# Cabin_num       10
# Side            11
# VIP_C           12  


HomePlanet = {'地球':0, '火星':1, '歐羅巴':2}
Destination = {'巨蟹座55e':0, '寶瓶座':1, 'PSO J318.5-22':2}
VIP_C1 = {'硬座':0, '硬臥':1}
VIP_C2 = {'硬座':0, '硬臥':1, '軟座(VIP)':2, '軟臥(VIP)':3}
spend_class = {'消費不起':0, '低消':1, '一般消費':2, '高端':3, '奢華':4 }
deck_0 = {'甲板 E':4, '甲板 F':5, '甲板 G':6}
deck_1 = {'甲板 D':3, '甲板 E':4, '甲板 F':5}
deck_2 = {'甲板 A':0, '甲板 B':1, '甲板 C':2, '甲板 D':3, '甲板 E':4, '甲板 T':7}
Cabin = {'艦首一':0, '艦首二':1, '艦身一':2, '艦身二':3, '艦身三':4, '艦身四':5, '艦尾二':6, '艦尾一':7}
col1, col2 = st.columns(2)
with col1:
    name = st.text_input('姓名')
    list1[0] = HomePlanet[st.selectbox('出發地', HomePlanet.keys())]
    list1[1] = Destination[st.selectbox('目的地', Destination.keys())]
    list1[2] = st.slider('年齡', value=12, min_value=0, max_value=80)
    list1[8] = st.slider('同行人數', value=0, min_value=0, max_value=7)

    if list1[0] == 0:
       list1[12] = VIP_C1[st.radio('艙等', VIP_C1.keys())]
    else:
       list1[12] = VIP_C2[st.radio('艙等', VIP_C2.keys())]

    if list1[0] == 0:
       list1[9] = deck_0[st.radio('甲板', deck_0.keys())]
    elif list1[0] == 1:
       list1[9] = deck_1[st.radio('甲板', deck_1.keys())]   
    else:
       list1[9] = deck_2[st.radio('甲板', deck_2.keys())]    
    list1[10] = Cabin[st.selectbox('客艙段', Cabin.keys())]
    list1[11] = 0 if st.radio("位置", options=('左舷側(P)', '右舷側(S)'))=='左舷側(P)' else 1 

with col2:    
    st.markdown(get_image_html("./image/ship.jpg"), unsafe_allow_html=True)
    if (list1[12] == 0 or list1[12] == 2):
        st.text('預期消費水平')
        list1[3] = spend_class[st.select_slider('客房服務',['消費不起','低消', '一般消費', '高端', '奢華'])]
        list1[4] = spend_class[st.select_slider('自助餐吧',['消費不起','低消', '一般消費', '高端', '奢華'])]
        list1[5] = spend_class[st.select_slider('購物中心',['消費不起','低消', '一般消費', '高端', '奢華'])]
        list1[6] = spend_class[st.select_slider('SPA',['消費不起','低消', '一般消費', '高端', '奢華'])]
        list1[7] = spend_class[st.select_slider('虛擬遊樂設施',['消費不起','低消', '一般消費', '高端', '奢華'])]

if st.button('預測'):
    if list1[2]  <= 12 :
        list1[2] = 0
    elif list1[2]  <= 24 :
        list1[2] = 1
    elif list1[2]  <= 36 :
        list1[2] = 2        
    elif list1[2]  <= 48 :
        list1[2] = 3
    elif list1[2]  <= 60 :
        list1[2] = 4         
    elif list1[2]  <= 72 :
        list1[2] = 5
    else:
        list1[2] = 6                
    list1[8] = list1[8]+1

    X_new = [list1]
    X_new = scaler.transform(X_new)
    if s_model.predict(X_new)[0] :
        st.write(f'### 預測結果： {name} 80%的機率 死定了！')
    else :
        st.write(f'### 預測結果： {name} 在倖存者名單上！')

